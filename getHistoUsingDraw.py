import ROOT


## create the TH1F plot using tree.Draw function
def getHistoUsingDraw(tree, histoOptions, cuts_weight, sampleName, isMC=True):
    expr = "%s >> histo(%s,%s,%s)"%(histoOptions.var,str(histoOptions.nbins),str(histoOptions.xmin),str(histoOptions.xmax))
    tree.Draw( expr, cuts_weight, histoOptions.opts)
#    print 'tree.Draw( "%s", "%s", "%s")'%( expr, cuts_weight, histoOptions.opts)
    histo = ROOT.gDirectory.Get("histo")
    ## debug in case of problems
    if type(histo)!=ROOT.TH1F:
        ROOT.gDirectory.ls()
        print tree.Draw("","")
        assert(type(histo)==ROOT.TH1F)
    histo.SetName(histoOptions.plotName+"_"+sampleName)
    return histo

## create the TH1F plot using looping the tree manually and evaluating the function defined as var
def getHistoUsingLoop(tree, histoOptions, cuts_weight, sampleName, isMC=True):
    histo = ROOT.TH1F(histoOptions.plotName+"_"+sampleName,"",histoOptions.nbins, histoOptions.xmin, histoOptions.xmax)
    weightForm = ROOT.TTreeFormula("weightFormula",cuts_weight,tree)
    function = histoOptions.var
    weight=1
    for event in tree:
        weight = weightForm.EvalInstance()
        if weight!=0:
            value = function(tree)
            histo.Fill(value,weight)
    return histo

## create the TH1F plot using tree.Draw function or looping on the tree
def getHisto(tree, histoOptions, sampleName, isMC=True):
    ## if defined, switch off all unused variables
    if len(histoOptions.treeVars)>0:
        tree.SetBranchStatus("*",0)
        for treeVar in histoOptions.treeVars:
            if treeVar!="" and not treeVar[0].isdigit():
                tree.SetBranchStatus(treeVar,1)
    
    ## cuts and weights are different for data and MC
    if isMC:
        cuts_weight = "(%s)*(%s)"%(histoOptions.cutsMC,histoOptions.weightMC)
    else:
        cuts_weight = "(%s)"%(histoOptions.cutsData)
    
    ## call getHistoUsingLoop or getHistoUsingDraw depending if var is a function
    if callable(histoOptions.var):
        return getHistoUsingLoop(tree, histoOptions, cuts_weight, sampleName, isMC)
    else:
        return getHistoUsingDraw(tree, histoOptions, cuts_weight, sampleName, isMC)
