import ROOT
from getHistoUsingDraw import getHisto
from array import array
### create the TH1F plot using tree.Draw function

doubleVariable = array('d',[0])
## create the THStack plot using tree.Draw function
def getStackWithDataOverlayAndLegend(leg, datasetMC, datasetData, groups, histoOptions):
    dataset = {}
    dataset.update(datasetMC)
    dataset.update(datasetData)
    totalMC = 0.
    totalData = 0.
    totalMC2_err = 0.
    dataPlot = None
    signalPlot = None
    stack = ROOT.THStack(histoOptions.plotName,'')
    for group in groups:
        print group.latexName
        firstSample = True
        if group.samples[0] in datasetMC:
            for sampleName in group.samples:
                sample = datasetMC[sampleName]
                tmp = getHisto(sample.tree, histoOptions, sampleName)
                tmp.Scale(sample.singleEventWeight)
                integral = tmp.IntegralAndError(1,tmp.GetNbinsX(),doubleVariable)
                print sampleName+":",round(integral,1)," +/- ",round(doubleVariable[0],1)
                totalMC += integral
                totalMC2_err += doubleVariable[0]**2
                if firstSample:
                    histo = tmp
                    histo.SetFillColor(group.color)
                    histo.SetLineColor(ROOT.kBlack)
                else:
                    histo.Add(tmp)
                firstSample = False
            stack.Add(histo)
            if group.latexName.lower() == "signal":
                print "copy signal for overlay"
                signalPlot = histo.Clone("Overlay")
                signalPlot.SetMarkerColor(signalPlot.GetLineColor())
            leg.AddEntry(histo,group.latexName+" (%s)"%str(round(histo.Integral(),1)),"f")
        elif group.samples[0] in datasetData:
            for sampleName in group.samples:
                sample = datasetData[sampleName]
                tmp = getHisto(sample.tree, histoOptions, sampleName, isMC=False)
                print sampleName+":",round(tmp.Integral(),1)
                if firstSample:
                    histo = tmp
                    histo.SetLineColor(ROOT.kBlack)
                else:
                    histo.Add(tmp)
                firstSample = False
            dataPlot=histo
            totalData += dataPlot.Integral()
        else:
            raise ValueError("Dataset %s in group %s is not defined in any DatasetMC nor DatasetData. The group and dataset checker does not work!"%(group.samples[0],group.latexName))
    
    print "Total MC:",round(totalMC,1)," +/- ",round((totalMC2_err**0.5),1)
    print "Total Data:",round(totalData,1)
    
    if histoOptions.normalized:
        ratio = totalData/totalMC
        for histo in stack.GetHists():
            histo.Scale(ratio)
    
    stack.Draw("goff")
    
    stack.GetXaxis().SetTitle(histoOptions.xTitle)
    stack.GetYaxis().SetTitle(histoOptions.yTitle)
    return stack,dataPlot,signalPlot

## create the TLegend
def createLegend():
    leg = ROOT.TLegend(0.75, 0.65,0.92,0.92)
    leg.SetLineWidth(2)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(62)
    leg.SetTextSize(0.035)
    return leg

## evaluate the ratio
def getRatio(data, stack, padSizeRatio):
    background = stack.GetStack().Last()
    backgroundNoError = background.Clone("backgroundNoError")
    for i in range(backgroundNoError.GetNbinsX()):
        backgroundNoError.SetBinError(i,0)
    ratio = data.Clone("ratio")
    ratio.Reset()
    
    ratio.GetYaxis().SetLabelSize(padSizeRatio*stack.GetYaxis().GetLabelSize())
    ratio.GetXaxis().SetLabelSize(padSizeRatio*data.GetXaxis().GetLabelSize())
    ratio.GetYaxis().SetTitleSize(padSizeRatio*stack.GetYaxis().GetTitleSize())
    ratio.GetXaxis().SetTitleSize(padSizeRatio*data.GetXaxis().GetTitleSize())
    ratio.GetYaxis().SetTitleOffset(1./padSizeRatio*stack.GetYaxis().GetTitleOffset())
    ratio.GetXaxis().SetTitleOffset(1./stack.GetXaxis().GetTitleOffset())
    ratio.GetYaxis().SetTitle("Data/MC")    
    ratio.GetXaxis().SetTitle(stack.GetXaxis().GetTitle())    
    ratio.GetYaxis().SetNdivisions(805)
    
    ratioMC = ratio.Clone("ratioMC")
    ratio.Divide(data,backgroundNoError)
    ratioMC.Divide(background,backgroundNoError)
    
    ratioMC.SetMarkerSize(0)
    for i in range(ratioMC.GetNbinsX()):
        x = ratioMC.GetBinContent(i)
        if x!=1:
            ratioMC.SetBinContent(i,1.)
            ratioMC.SetBinError(i,10.)
    
    ratioMC.SetFillStyle(3001)
    ratioMC.SetFillColor(ROOT.kGray)
        
    return ratio, ratioMC
