from glob import glob
import ROOT
import array
import os,sys

printLineNull = True
printLineSignif = True
printLineSignifN = True

def getROC(background, signal):
    xaxis = background.GetXaxis()
    xaxis_check = signal.GetXaxis()
    assert ( xaxis.GetNbins()==xaxis_check.GetNbins() and xaxis.GetXmax()==xaxis_check.GetXmax() and xaxis.GetXmin()==xaxis_check.GetXmin() )
    nbins = xaxis.GetNbins()
    
    bkg_tot = background.Integral(0,nbins+1)
    sig_tot = signal.Integral(0,nbins+1)
    ## nbins+3: first bin zero + nbins + overflow + underflow
    bkg_int = [0]*(nbins+3)
    sig_int = [0]*(nbins+3)
    sig_eff = [0]*(nbins+3)
    bkg_rej = [0]*(nbins+3)
    for i in range(1,nbins+3):
        sig_int[i] = (sig_int[i-1]+signal.GetBinContent(i-1))
        bkg_int[i] = (bkg_int[i-1]+background.GetBinContent(i-1))
    
#    ## possible check
#    print bkg_int[nbins+2],"=",background.Integral(0,nbins+1)
#    print sig_int[nbins+2],"=",signal.Integral(0,nbins+1)
    
    bkg_tot = bkg_int[nbins+2]
    sig_tot = sig_int[nbins+2]

    bestS2_B = -3
    bestCut = 0
    inverted = True
    for i in range(0,nbins+3):
        sig_eff[i] = sig_int[i]/sig_tot
        bkg_rej[i] = 1 - bkg_int[i]/bkg_tot
        if inverted:
            sig_eff[i] = 1 - sig_eff[i]
            bkg_rej[i] = 1 - bkg_rej[i]
        ## find the best cuts (highest eff/sqrt(1-rej) or eff**2/(1-rej))
        S2_B = sig_eff[i]*sig_eff[i]/(1.0001-bkg_rej[i])
        if S2_B>bestS2_B:
            bestCut = xaxis.GetBinLowEdge(i)
            bestS2_B = S2_B
#        print "sig_eff[i]:",sig_eff[i],
#        print "\tbkg_rej[i]:",bkg_rej[i]
#        print "\tvalue:",xaxis.GetBinCenter(i)

    if bestS2_B>1.01:
        print "Best cut: ",bestCut,"\timprove S/sqrt(B) of: ",(bestS2_B)**0.5,
#    print "bkg_tot: ",bkg_tot,"\tsig_tot: ",sig_tot,
    arrX, arrY = array.array('f',sig_eff),array.array('f',bkg_rej)
    ROC = ROOT.TGraph( len(sig_eff) , arrX, arrY )
    ROC.SetLineColor(ROOT.kRed)
    ROC.SetLineWidth(3)
    ROC.SetTitle("")
    ROC.GetXaxis().SetTitle("Signal efficiency")
    ROC.GetYaxis().SetTitle("Background rejection")
    
    return ROC,bestS2_B

def doROC(fileName):
    print "I'm doing ",fileName
    file_ = ROOT.TFile(fileName)
    c1 = file_.Get("c2")
    list_ = c1.GetListOfPrimitives()[1].GetListOfPrimitives()
    stack = list_[1]
    background = stack.GetStack().Last().Clone("background")
    signal = list_[2]
    roc,bestS2_B = getROC(background,signal)
    c2 = ROOT.TCanvas()
    c2.SetGridx()
    c2.SetGridy()
    roc.Draw("AP")
    
    if printLineNull:
        lineNull = ROOT.TF1("lineNull","1-x",0,1)
        lineNull.SetLineColor(ROOT.kBlack)
        lineNull.SetLineStyle(2)
        lineNull.Draw("same")
    
    if printLineSignif:
        lineSignif = ROOT.TF1("lineSignif","1-x**2",0,1)
        lineSignif.SetLineColor(ROOT.kBlack)
        lineSignif.SetLineStyle(2)
        lineSignif.Draw("same")
    
    if printLineSignifN:
        N = (bestS2_B)**0.5
        lineSignifN = ROOT.TF1("lineSignifN","1-(x/%s)**2"%N,0,1)
        lineSignifN.SetLineColor(ROOT.kBlack)
        lineSignifN.SetLineStyle(2)
        lineSignifN.Draw("same")

    roc.Draw("L")
    folder = fileName.split("/")[:-1]
    folder[-1] = "ROC"
    folder = '/'.join(folder)
    name = fileName.split("/")[-1]
    os.system("mkdir -p %s"%folder)
    
    folder = folder+"/root"
    outputFileName = folder+"/"+name
    os.system("mkdir -p %s"%folder)
    c2.SaveAs(folder+"/"+name)
    
    folder = folder.replace("root","png")
    name = name.replace("root","png")
    os.system("mkdir -p %s"%folder)
    c2.SaveAs(folder+"/"+name)
    
    folder = folder.replace("png","pdf")
    name = name.replace("png","pdf")
    os.system("mkdir -p %s"%folder)
    c2.SaveAs(folder+"/"+name)

if __name__ == "__main__":
    ROOT.gROOT.SetBatch()
    inputFiles = sys.argv[1:]
    print "Input files: ", inputFiles
    
    for inputFile in inputFiles:
        files = glob(inputFile) ## solve possible wildcard characters
        for file_ in files:
            doROC(file_)
            print "\n"


#    doROC("plotsDec24/SumCSVnjetsbtagCSV1IterationLength.root")
#    doROC("plotsDec24/SumCSVnjetsbtagCSV2IterationLength.root")
#    doROC("plotsDec24/SumCSVnjetsbtagCSV3IterationLength.root")
#    doROC("plotsDec24/SumCSVnjetsbtagCSV4IterationLength.root")

#    doROC("plotsDec24/btagLRgeq2bleq1bbtagCSV.root")
#    doROC("plotsDec24/btagLR4b2bbtagCSV.root")
#    doROC("plotsDec24/btagLR3b2bbtagCSV.root")
#    doROC("plotsDec24/btagLR4b3bbtagCSV.root")

#    doROC("plotsDec24/SumCSVnjetsqgl1IterationLength.root")
#    doROC("plotsDec24/SumCSVnjetsqgl2IterationLength.root")
#    doROC("plotsDec24/SumCSVnjetsqgl3IterationLength.root")
#    doROC("plotsDec24/SumCSVnjetsqgl4IterationLength.root")

#    doROC("plotsDec24/qgLR4bflavour3q0q.root")
#    doROC("plotsDec24/qgLR4bflavour4q0q.root")
#    doROC("plotsDec24/qgLR4bflavour4q3q.root")
#    doROC("plotsDec24/qgLR4bflavour5q4q.root")

#    doROC("plotsDec24/qgLR3bflavour3q0q.root")
#    doROC("plotsDec24/qgLR3bflavour3q2q.root")
#    doROC("plotsDec24/qgLR3bflavour4q0q.root")
#    doROC("plotsDec24/qgLR3bflavour4q3q.root")

#    doROC("plotsDec24/root/logmemtthFH1w1w2h2tp.root")
#    doROC("plotsDec24/root/logmemttbbFH1w1w2h2tp.root")
#    doROC("plotsDec24/root/memtthFH1w1w2h2tpmemttbbFH1w1w2h2tpmemtthFH1w1w2h2tp.root")

    '''
    doROC("preselection/SumCSVnjetsqgl2IterationLength.root")
    doROC("preselection/Altjetspt50.root")
    doROC("preselection/Altjetspt60.root")
    doROC("preselection/Altjetspt70.root")
    doROC("preselection/Altjetspt80.root")
    doROC("preselection/SumCSVnjetsbtagCSV2IterationLength.root")
    doROC("preselection/SumCSVnjetsbtagCSV3IterationLength.root")
    doROC("preselection/SumCSVnjetsqgl2IterationLength.root")
    doROC("preselection/SumCSVnjetsqgl3IterationLength.root")
    doROC("preselection/SumCSVnjetsqgl4IterationLength.root")
    doROC("preselection/btagLR3b2bbtagCSV.root")
    doROC("preselection/btagLR4b2bbtagCSV.root")
    doROC("preselection/btagLR4b3bbtagCSV.root")
    doROC("preselection/btagLRgeq2bleq1bbtagCSV.root")
    doROC("preselection/ht.root")
    doROC("preselection/qgLR3bflavour3q0q.root")
    doROC("preselection/qgLR3bflavour3q2q.root")
    doROC("preselection/qgLR3bflavour4q0q.root")
    doROC("preselection/qgLR3bflavour4q3q.root")
    doROC("preselection/qgLR3bflavour5q4q.root")
    doROC("preselection/qgLR4bflavour3q0q.root")
    doROC("preselection/qgLR4bflavour3q2q.root")
    doROC("preselection/qgLR4bflavour4q0q.root")
    doROC("preselection_2btag/Altjetspt50.root")
    doROC("preselection_2btag/Altjetspt60.root")
    doROC("preselection_2btag/Altjetspt70.root")
    doROC("preselection_2btag/Altjetspt80.root")
    doROC("preselection_2btag/SumCSVnjetsbtagCSV2IterationLength.root")
    doROC("preselection_2btag/SumCSVnjetsbtagCSV3IterationLength.root")
    doROC("preselection_2btag/SumCSVnjetsqgl2IterationLength.root")
    doROC("preselection_2btag/SumCSVnjetsqgl3IterationLength.root")
    doROC("preselection_2btag/SumCSVnjetsqgl4IterationLength.root")
    doROC("preselection_2btag/btagLR3b2bbtagCSV.root")
    doROC("preselection_2btag/btagLR4b2bbtagCSV.root")
    doROC("preselection_2btag/btagLR4b3bbtagCSV.root")
    doROC("preselection_2btag/btagLRgeq2bleq1bbtagCSV.root")
    doROC("preselection_2btag/ht.root")
    doROC("preselection_2btag/qgLR3bflavour3q0q.root")
    doROC("preselection_2btag/qgLR3bflavour3q2q.root")
    doROC("preselection_2btag/qgLR3bflavour4q0q.root")
    doROC("preselection_2btag/qgLR3bflavour4q3q.root")
    doROC("preselection_2btag/qgLR3bflavour5q4q.root")
    doROC("preselection_2btag/qgLR4bflavour3q0q.root")
    doROC("preselection_2btag/qgLR4bflavour3q2q.root")
    doROC("preselection_2btag/qgLR4bflavour4q0q.root")
    doROC("preselection_noCuts/Altjetspt50.root")
    doROC("preselection_noCuts/Altjetspt60.root")
    doROC("preselection_noCuts/Altjetspt70.root")
    doROC("preselection_noCuts/Altjetspt80.root")
    doROC("preselection_noCuts/SumCSVnjetsbtagCSV3IterationLength.root")
    doROC("preselection_noCuts/SumCSVnjetsqgl2IterationLength.root")
    doROC("preselection_noCuts/SumCSVnjetsqgl3IterationLength.root")
    doROC("preselection_noCuts/SumCSVnjetsqgl4IterationLength.root")
    doROC("preselection_noCuts/btagLR3b2bbtagCSV.root")
    doROC("preselection_noCuts/btagLR4b2bbtagCSV.root")
    doROC("preselection_noCuts/btagLR4b3bbtagCSV.root")
    doROC("preselection_noCuts/btagLRgeq2bleq1bbtagCSV.root")
    doROC("preselection_noCuts/ht.root")
    doROC("preselection_noCuts/qgLR3bflavour3q0q.root")
    doROC("preselection_noCuts/qgLR3bflavour3q2q.root")
    doROC("preselection_noCuts/qgLR3bflavour4q0q.root")
    doROC("preselection_noCuts/qgLR3bflavour4q3q.root")
    doROC("preselection_noCuts/qgLR3bflavour5q4q.root")
    doROC("preselection_noCuts/qgLR4bflavour3q0q.root")
    doROC("preselection_noCuts/qgLR4bflavour3q2q.root")
    doROC("preselection_noCuts/qgLR4bflavour4q0q.root")
    '''
#    file_ = ROOT.TFile("preselection/SumCSVnjetsqgl2IterationLength.root")
#    c1 = file_.Get("c1")
#    list_ = c1.GetListOfPrimitives()
#    stack = c1.GetListOfPrimitives()[1]
#    background = stack.GetStack().Last().Clone("background")
#    signal = c1.GetListOfPrimitives()[3]
#    roc = getROC(background,signal)
#    c2 = ROOT.TCanvas()
#    roc.Draw("APL")
#    print background.Integral(background.FindBin(0.9),background.GetXaxis().GetNbins()+1)/background.Integral(-1,background.GetXaxis().GetNbins()+1)
#    print signal.Integral(signal.FindBin(0.9),signal.GetXaxis().GetNbins()+1)/signal.Integral(-1,signal.GetXaxis().GetNbins()+1)


