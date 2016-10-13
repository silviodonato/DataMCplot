import ROOT

## create the TH1F plot using tree.Draw function
def getHistoUsingDraw(tree, histoOptions):
    (var, nbins, xmin, xmax, weight, cuts, opts,sampleName) = histoOptions
    expr = "%s >> histo(%s,%s,%s)"%(var,str(nbins),str(xmin),str(xmax))
    cuts_weight = "(%s)*(%s)"%(cuts,weight)
    tree.Draw( expr, cuts_weight, opts)
    histo = ROOT.gDirectory.Get("histo")
    if type(histo)!=ROOT.TH1F:
        ROOT.gDirectory.ls()
        print tree.Draw("","")
        assert(type(histo)==ROOT.TH1F)
    histo.SetName(var)
    return histo
