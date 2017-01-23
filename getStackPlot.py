import ROOT
from getHistoUsingDraw import getHisto
from array import array
### create the TH1F plot using tree.Draw function

doubleVariable = array('d',[0])

## print histogram yields
def printYield(histo):
    integral = histo.IntegralAndError(1,histo.GetNbinsX(),doubleVariable)
    output = str(round(integral,1))
    output += " +/- "+str(round(doubleVariable[0],1))
    output += " [u:"+str(round(histo.GetBinContent(0),1))+" ,"
    output += "o:"+str(round(histo.GetBinContent(histo.GetNbinsX()+1),1))+"]"
    return output

## create the THStack plot using tree.Draw function
def getStackWithDataOverlayAndLegend(leg, datasets, groups, histoOptions):
    dataPlot = None
    signalPlot = None
    nbackgroundFromData = 0
    stack = ROOT.THStack(histoOptions.plotName,'')
    for group in groups:
        print group.latexName
        firstSample = True
        if group.type in ["background","signal","backgroundFromData"]:
            for sampleName in group.samples:
                histoOptions_ = histoOptions
                sample = datasets[sampleName]
                if group.type is "backgroundFromData": ##add "weight" if it is a data driven background
                    histoOptions_ = histoOptions.clone(weightMC="(%s!=1)*%s*%s+(%s==1)"%(sample.weight, sample.weight, histoOptions.weightMC, sample.weight))
                    nbackgroundFromData += 1
                isMC = True
                tmp = getHisto(sample.tree, histoOptions_, sampleName, isMC)
                tmp.Scale(sample.singleEventWeight)
                integral = tmp.IntegralAndError(1,tmp.GetNbinsX(),doubleVariable)
                print sampleName+":",round(integral,1)," +/- ",round(doubleVariable[0],1),"[u:",round(tmp.GetBinContent(0),1)," ,o:",round(tmp.GetBinContent(tmp.GetNbinsX()+1),1),"]"
                if firstSample:
                    histo = tmp
                    histo.SetFillColor(group.color)
                    histo.SetLineColor(ROOT.kBlack)
                    histo.SetName(histoOptions.plotName+"_"+group.name)
                else:
                    histo.Add(tmp)
                firstSample = False
            stack.Add(histo)
            if group.type == "signal":
                print "copy signal for overlay"
                signalPlot = histo.Clone("Overlay")
                signalPlot.SetMarkerColor(signalPlot.GetLineColor())
#            leg.AddEntry(histo,group.latexName+" (%s)"%str(round(histo.Integral(),1)),"f")
        elif group.type in ["data"]:
                for sampleName in group.samples:
                    sample = datasets[sampleName]
                    tmp = getHisto(sample.tree, histoOptions, sampleName, isMC=False)
                    print sampleName+":",round(tmp.Integral(),1),"[u:",round(tmp.GetBinContent(0),1)," ,o:",round(tmp.GetBinContent(tmp.GetNbinsX()+1),1),"]"
                    if firstSample:
                        histo = tmp
                        histo.SetLineColor(ROOT.kBlack)
                    else:
                        histo.Add(tmp)
                    firstSample = False
                dataPlot=histo
        else:
            raise ValueError("Dataset %s in group %s is not defined in any DatasetMC nor DatasetData. The group and dataset checker does not work!"%(group.samples[0],group.latexName))
    
    totalMC = stack.GetStack().Last().Integral()
    totalData = 0.
    if dataPlot:
        totalData = dataPlot.Integral()
    
    normOpt = histoOptions.normalized
    hists = stack.GetHists()
    ## if normalize the data-drive samples in order to get yield(MC)==yield(data)
    if nbackgroundFromData>0:
        if nbackgroundFromData>1:
            raise Exception("You have %s data-driven background groups. It can be only one!"%(str(nbackgroundFromData)))
        ## get the rescaling factor and scale the data-driven background
        integral = 0
        for group in groups:
            if group.type is "backgroundFromData":
                histo = hists.FindObject(histoOptions.plotName+"_"+group.name)
                sample_name = histo.GetName().split("_")[1]
                integral += histo.Integral()
                correction = 1.+(totalData-totalMC)/(integral+1E-6)
                print "I'm correcting ",sample_name," by a factor ",correction
                histo.Scale(correction)
    
    ## normalize MC to data, if requested
    if normOpt is True:
            ratio = totalData/totalMC
            for histo in hists:
                histo.Scale(ratio)
            print "Normalizing MC to data. Ratio:",ratio
    
    ## Print histrogram yields
    stack.Modified()
    print
    print "### Histogram yields: ###"
    for histo in hists:
        sampleName = histo.GetName().split("_")[1]
        print sampleName+": "+printYield(histo)
    
    print
    print "### Total MC: "+printYield(stack.GetStack().Last())+" ###"
    
    if dataPlot:
        print
        print "### Total Data: "+printYield(dataPlot)+" ###"
    
    if signalPlot:
        print
        print "### Total Signal: "+printYield(signalPlot)+" ###"
    
    ## fill legend
    for group in groups:
        if not group.type is "data":
            histo = hists.FindObject(histoOptions.plotName+"_"+group.name)
            groupIntegral = histo.Integral()
            leg.AddEntry(histo,group.latexName+" (%s)"%str(round(groupIntegral,1)),"f")
    
    ## set x and y plot label
    stack.Draw("goff")
    
    stack.GetXaxis().SetTitle(histoOptions.xTitle)
    stack.GetYaxis().SetTitle(histoOptions.yTitle)
    
    ## if we are blinded, set dataPlot to zero
    if histoOptions.blinded:
        dataPlot.Reset()
    
    ## return objects
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
    ratioMC.SetFillColor(ROOT.kGray+1)
        
    return ratio, ratioMC
