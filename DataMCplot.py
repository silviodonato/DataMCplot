import TdrStyles
import string
import ROOT
import os
from math import *
from copy import *
from array import array
from config import histos,datasetMC,datasetData,groups,userFunctions
from getStackPlot import getStackWithDataOverlayAndLegend,createLegend
import time
from optparse import OptionParser

#parser = OptionParser()
#parser.add_option("-c", "--config", dest="config", default="config.py"
#                  help="config file") #, metavar="FILE"
#(options, args) = parser.parse_args()

#histos = importlib.import_module(options.config)
#from config import histos,datasetMC,datasetData,groups,userFunctions

for userFunction in userFunctions:
    ROOT.gROOT.LoadMacro(userFunction)

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

for histoOptions in histos:
    t0 = time.time()
    print 
    print histoOptions.var
    print 
    TdrStyles.tdrStyle()
    legend = createLegend()
    stack,dataPlot,signalPlot = getStackWithDataOverlayAndLegend(legend,datasetMC,datasetData, groups, histoOptions)

    c1 = ROOT.TCanvas("c1","",1280,720)
    stack.SetMaximum(max(stack.GetMaximum(),dataPlot.GetMaximum())*1.3)
    stack.Draw("HIST")
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
#        scaleOverlay = getOverlayScale(signalPlot,stack)
        scaleOverlay = getOverlayScale(signalPlot,dataPlot)
#        scaleOverlay = getOverlayScale(signalPlot,stack)
        signalPlot.Scale(scaleOverlay)
        signalPlot.Draw("same")
        legend.AddEntry(signalPlot,"signal x %s"%str(scaleOverlay),"l")
    legend.Draw()
    os.system("mkdir -p %s"%histoOptions.folder)
    outputName = histoOptions.folder+"/"+histoOptions.plotName+".png"
    c1.SaveAs(outputName)
    c1.SaveAs(outputName.replace(".png",".root"))
    print outputName+" saved"
    print "Time consuming: ",round(time.time() - t0,1)," s."

