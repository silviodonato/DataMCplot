import ROOT

## create the TH1F plot using tree.Draw function
def getHistoUsingDraw(tree, histoOptions, isMC=True):
    if isMC:
        cuts_weight = "(%s)*(%s)"%(histoOptions.cutsMC,histoOptions.weightMC)
    else:
        cuts_weight = "(%s)"%(histoOptions.cutsData)
    expr = "%s >> histo(%s,%s,%s)"%(histoOptions.var,str(histoOptions.nbins),str(histoOptions.xmin),str(histoOptions.xmax))
    tree.Draw( expr, cuts_weight, histoOptions.opts)
    histo = ROOT.gDirectory.Get("histo")
    if type(histo)!=ROOT.TH1F:
        ROOT.gDirectory.ls()
        print tree.Draw("","")
        assert(type(histo)==ROOT.TH1F)
    histo.SetName(histoOptions.plotName)
    
    return histo

## create the THStack plot using tree.Draw function
def getStackWithDataOverlayAndLegend(leg, datasetMC, datasetData, groups, histoOptions):
    dataset = {}
    dataset.update(datasetMC)
    dataset.update(datasetData)
    dataPlot = None
    signalPlot = None
    stack = ROOT.THStack(histoOptions.plotName,'')
    for group in groups:
        print group.latexName
        firstSample = True
        if group.samples[0] in datasetMC:
            for sampleName in group.samples:
                sample = datasetMC[sampleName]
                tmp = getHistoUsingDraw(sample.tree, histoOptions)
                tmp.Scale(sample.singleEventWeight)
                print sampleName+":",round(tmp.Integral(),1)
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
            leg.AddEntry(histo,group.latexName+" (%s)"%str(round(histo.Integral(),1)),"f")
        elif group.samples[0] in datasetData:
            for sampleName in group.samples:
                sample = datasetData[sampleName]
                tmp = getHistoUsingDraw(sample.tree, histoOptions, isMC=False)
                print sampleName+":",round(tmp.Integral(),1)
                if firstSample:
                    histo = tmp
                    histo.SetLineColor(ROOT.kBlack)
                else:
                    histo.Add(tmp)
                firstSample = False
            dataPlot=histo
        else:
            raise ValueError("Dataset %s in group %s is not defined in any DatasetMC nor DatasetData. The group and dataset checker does not work!"%(group.samples[0],group.latexName))
    
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
    leg.SetFillStyle(4000)
    leg.SetTextFont(62)
    leg.SetTextSize(0.035)
    return leg
