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
config = importlib.import_module('configs.'+options.config.replace(".py",""))
print "I'm using "+options.config+" as configuration in configs folder."
print ""
for el in ['histos','datasetMC','datasetData','groups','userFunctions']:
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

## run in batch mode, if requested
if options.batch:
    ROOT.gROOT.SetBatch()

## load ROOT functions
for userFunction in userFunctions:
    ROOT.gROOT.LoadMacro(userFunction)

## define a function to find the optimal overlay scale
def getOverlayScale(signalPlot,stack):
    maxSig = signalPlot.GetMaximum()
    maxStack = stack.GetMaximum()
    scale = str(maxStack/maxSig).split(".")[0]
    scale = int(scale[0])*(10**len(scale))/10
    return int(scale)

## Check the definition of the groups and datasets, load the trees, and get the totalLumi
totalLumi = 0
for group in groups:
    if len(group.samples)==0:
        raise ValueError("Group %s contains zero samples. Please fix it."%group.latexName)
    for sample in group.samples:
        if sample in datasetData:
            datasetData[sample].loadTree()
            totalLumi += datasetData[sample].lumi
        elif sample in datasetMC:
            datasetMC[sample].loadTree()
        else:
            raise ValueError("Dataset %s in group %s is not defined in any DatasetMC nor DatasetData."%(sample,group.latexName))

## Evaluate the normalization to be applied to each simulated event
for mc in datasetMC.values(): 
    if hasattr(mc,"tree"):
        mc.setSingleEventWeight(totalLumi)

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
    
    stack,dataPlot,signalPlot = getStackWithDataOverlayAndLegend(legend,datasetMC,datasetData, groups, histoOptions)
    padSizeRatio = (padPlot.GetWh()*padPlot.GetAbsHNDC())/(padRatio.GetWh()*padRatio.GetAbsHNDC())

    stack.GetHistogram().GetXaxis().SetTickLength(0)
    stack.GetHistogram().GetXaxis().SetLabelSize(0)
    stack.GetHistogram().GetXaxis().SetTitleSize(0)

    stack.SetMaximum(max(stack.GetMaximum(),dataPlot.GetMaximum())*1.3)
    stack.Draw("HIST")
    print stack.GetXaxis().GetLabelSize()
    if dataPlot:
        dataPlot.SetMarkerStyle(20) 
        dataPlot.SetMarkerSize(1.2)
        dataPlot.Draw("same,E1")
        legend.AddEntry(dataPlot,"data (%s)"%str(int(dataPlot.Integral())),"P")
    if signalPlot:
        signalPlot.SetLineWidth(3)
        signalPlot.SetLineColor(ROOT.kBlue)
        signalPlot.SetMarkerColor(ROOT.kBlue)
        signalPlot.SetFillStyle(0)
        scaleOverlay = getOverlayScale(signalPlot,dataPlot)
        signalPlot.Scale(scaleOverlay)
        signalPlot.Draw("same")
        legend.AddEntry(signalPlot,"signal x %s"%str(scaleOverlay),"l")
    
    legend.Draw()
    
    padRatio.cd()
    
    ratio,mcError = getRatio(dataPlot,stack,padSizeRatio)
    print stack.GetXaxis().GetLabelSize()
    print dataPlot.GetXaxis().GetLabelSize()
    mcError.SetMaximum(1.499)
    mcError.SetMinimum(0.501)
    mcError.Draw("E3")
    ratio.Draw("E1,same")
    
    os.system("mkdir -p %s"%histoOptions.folder)
    outputName = histoOptions.folder+"/"+histoOptions.plotName+".png"
    c2.SaveAs(outputName)
    c2.SaveAs(outputName.replace(".png",".root"))
    print outputName+" saved"
    print "Time consuming: ",round(time.time() - t0,1)," s."

