#!/usr/bin/env python2.7
## load the config file
print ""
from optparse import OptionParser
import os
parser = OptionParser()
parser.add_option("-c", "--config", dest="config", default="configs/config_default.py",
                  help="set config file (default is config_default.py)")
parser.add_option("--gc",
                  action="store_true", dest="forGC", default=False,
                  help="to run with grid-control")
parser.add_option("-b", "--batch",
                  action="store_true", dest="batch", default=False,
                  help="run in batch mode")
(options, args) = parser.parse_args()

## if it is a grid-control job, load the environment variables
if options.forGC:
    config = os.environ['config']
    options.config = config
    histo_total = int(os.environ['histo_total'])
    histo_i = int(os.environ['histo_i'])
    
## load the proper "config" library#########
import importlib
print "I'm using "+options.config+" as configuration in configs folder."
print ""
options.config = options.config.replace("configs/","")
config = importlib.import_module('configs.'+options.config.replace(".py",""))
for el in ['histos','datasets','groups','userFunctions']:
    globals()[el]= getattr(config,el)

## import libraries
import TdrStyles
import string
import ROOT
import os
from math import *
from copy import *
from array import array
from getStackPlot import getStackWithDataOverlayAndLegend,createLegend,getRatio
import time
from getROC import doROC

## run in batch mode, if requested
if options.batch:
    ROOT.gROOT.SetBatch()

## load ROOT functions
for userFunction in userFunctions:
    ROOT.gROOT.LoadMacro(userFunction)

def printObj(text_file, obj, objName):
    for el in dir(obj):
        value = getattr(obj,el)
        if "__" in el or callable(value):
            pass
        elif isinstance(value, (int, long, float, complex, bool, set, list)):
            text_file.write('%s.%s = %s\n'%(objName,el,value))
        elif isinstance(value, (str)):
            text_file.write('%s.%s = "%s"\n'%(objName,el,value))

## define a function that print out the configuration used for each plot
def printConf(histoOptions,datasets,groups, outputFileName):
    text_file = open(outputFileName, "w")
    text_file.write("from Classes import DatasetMCClass,DatasetDataClass,DatasetDataDrivenClass,GroupClass,HistogramClass \n") 
    text_file.write("\n") 
    text_file.write("histoOptions = HistogramClass()\n") 
    printObj(text_file,histoOptions,"histoOptions")
    text_file.write("\n") 

    text_file.write("datasets = {}\n") 
    for dataset in datasets:
        text_file.write('datasets["%s"] = %s()\n'%(dataset,datasets[dataset].__class__.__name__)) 
        printObj(text_file,datasets[dataset],'datasets["%s"]'%dataset)
    text_file.write("\n") 

    text_file.write("groups = [0]*%s\n"%len(groups)) 
    for i in range(len(groups)):
        text_file.write("groups[%s] = %s()\n"%(str(i),groups[i].__class__.__name__)) 
        printObj(text_file,groups[i],"groups[%s]"%str(i))
    text_file.write("\n") 

    text_file.close()

## define a function to find the optimal overlay scale
def getOverlayScale(signalPlot,stack):
    maxSig = signalPlot.GetMaximum() + 1E-9
    maxStack = stack.GetMaximum() + 1E-9
    print "maxStack: ",maxStack
    print "maxSig: ",maxSig
    scale = str(maxStack/maxSig).split(".")[0]
    scale = int(scale[0])*(10**len(scale))/10
    return int(scale)

## Check the definition of the groups and datasets, load the trees, and get the totalLumi
totalLumi = 0
for group in groups:
    if len(group.samples)==0:
        raise ValueError("Group %s contains zero samples. Please fix it."%group.latexName)
    for sample in group.samples:
        if sample in datasets:
            datasets[sample].loadTree()
            if group.type is "data":
                totalLumi += datasets[sample].lumi
        else:
            raise ValueError("Dataset %s in group %s is not defined among datasets."%(sample,group.latexName))

#if there is no data, normalize MC to 40fb-1
if totalLumi==0: totalLumi=40000

#add a label with the lumi
ROOT.gROOT.LoadMacro("CMS_lumi.C")
ROOT.gROOT.ProcessLine('lumi_7TeV = "%s fb^{-1}";'%(round(totalLumi/1000,1)))
ROOT.gROOT.ProcessLine('extraText="Preliminary"')

## Evaluate the normalization to be applied to each simulated event
for dataset in datasets.values(): 
    if hasattr(dataset,"tree") and hasattr(dataset,"setSingleEventWeight"):
        dataset.setSingleEventWeight(totalLumi)

## if it is a grid-control job, select which histos to run in this job
print len(histos)
print len(config.histos)
if options.forGC:
    job_histos = []
    for i in range(len(histos)):
        if (i-histo_i)%histo_total == 0:
            job_histos.append(histos[i])
    histos = job_histos

## for each histograms plot the stack, data, signal overlay, legend and save the output
for histoOptions in histos:
    yPadSeparation = 0.25
    t0 = time.time()
    print 
    print histoOptions.var
    print 
    TdrStyles.tdrStyle()
    legend = createLegend()
    c2 = ROOT.TCanvas("c2","",1280,1024)
    c2.Draw()
    padPlot = ROOT.TPad("padPlot","",0.,yPadSeparation,1.,1.)
    padPlot.SetBottomMargin(.02)
    padRatio = ROOT.TPad("padRatio","",0.,0.,1.,yPadSeparation)
    padRatio.SetTopMargin(0)
    padRatio.SetBottomMargin(.09/yPadSeparation)
    padRatio.Draw()
    padPlot.Draw()
    padRatio.SetGridx()
    padRatio.SetGridy()
    padPlot.SetGridx()
    padPlot.SetGridy()
    padPlot.cd()
    
    stack,dataPlot,signalPlot = getStackWithDataOverlayAndLegend(legend,datasets, groups, histoOptions)
    padSizeRatio = (padPlot.GetWh()*padPlot.GetAbsHNDC())/(padRatio.GetWh()*padRatio.GetAbsHNDC())

    stack.GetHistogram().GetXaxis().SetTickLength(0)
    stack.GetHistogram().GetXaxis().SetLabelSize(0)
    stack.GetHistogram().GetXaxis().SetTitleSize(0)

    stack.Draw("HIST")
    if signalPlot:
        signalPlot.SetLineWidth(3)
        signalPlot.SetLineColor(ROOT.kBlue)
        signalPlot.SetMarkerColor(ROOT.kBlue)
        signalPlot.SetFillStyle(0)
        scaleOverlay = getOverlayScale(signalPlot,stack)
        signalPlot.Scale(scaleOverlay)
        signalPlot.Draw("same")
        legend.AddEntry(signalPlot,"signal x %s"%str(scaleOverlay),"l")
        if not dataPlot:
            dataPlot = signalPlot.Clone("dataPlot")
            dataPlot.Reset()
    if dataPlot.Integral()>0:
        stack.SetMaximum(max(stack.GetMaximum(),dataPlot.GetMaximum())*1.5)
        dataPlot.SetMarkerStyle(20) 
        dataPlot.SetMarkerSize(1.2)
        dataPlot.Draw("same,E1")
        legend.AddEntry(dataPlot,"data (%s)"%str(int(dataPlot.Integral())),"P")
    
    print stack.GetXaxis().GetLabelSize()
    
    legend.Draw()
    ROOT.CMS_lumi(padPlot)
    
    padRatio.cd()
    
    ratio,mcError = getRatio(dataPlot,stack,padSizeRatio)
    print stack.GetXaxis().GetLabelSize()
    print dataPlot.GetXaxis().GetLabelSize()
    mcError.SetMaximum(1.499)
    mcError.SetMinimum(0.501)
    mcError.Draw("E3")
    ratio.Draw("E1,same")
    
    
    os.system("mkdir -p %s"%histoOptions.folder)
    os.system("mkdir -p %s/png"%histoOptions.folder)
    outputName = histoOptions.folder+"/png/"+histoOptions.plotName+".png"
    c2.SaveAs(outputName)
    os.system("mkdir -p %s/root"%histoOptions.folder)
    c2.SaveAs(outputName.replace("png","root"))
    os.system("mkdir -p %s/pdf"%histoOptions.folder)
    c2.SaveAs(outputName.replace("png","pdf"))
    os.system("mkdir -p %s/conf"%histoOptions.folder)
    outputConf = outputName.replace("png","conf")
    outputConf = outputConf.replace(".conf",".py")
    printConf(histoOptions,datasets,groups,outputConf)
    print outputName+" saved"
    print "Time consuming: ",round(time.time() - t0,1)," s."
    
    print '\nLaunching doROC("%s")\n'%(outputName.replace("png","root"))
    doROC(outputName.replace("png","root"))
