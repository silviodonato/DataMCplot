import ROOT
import array


def getROC(background, signal):
    xaxis = background.GetXaxis()
    xaxis_check = signal.GetXaxis()
    assert ( xaxis.GetNbins()==xaxis_check.GetNbins() and xaxis.GetXmax()==xaxis_check.GetXmax() and xaxis.GetXmin()==xaxis_check.GetXmin() )
    
    bkg_int = background.GetIntegral()
    sig_int = signal.GetIntegral()
    sig_eff = []
    bkg_rej = []
    inverted = True
    for i in range(xaxis.GetNbins()+1):
        if inverted:
            sig_int[i] = 1 - sig_int[i]
            bkg_int[i] = 1 - bkg_int[i]
        sig_eff.append(sig_int[i]) 
        bkg_rej.append(1.-bkg_int[i]) 
#        print sig_int[i], bkg_int[i]
    
    
    arrX, arrY = array.array('f',sig_eff),array.array('f',bkg_rej)
    ROC = ROOT.TGraph( len(sig_eff) , arrX, arrY )
    ROC.SetLineColor(ROOT.kRed)
    ROC.SetLineWidth(3)
    ROC.SetTitle("")
    ROC.GetXaxis().SetTitle("Signal efficiency")
    ROC.GetYaxis().SetTitle("Background rejection")
    
    return ROC

def doROC(fileName):
    print "I'm doing ",fileName
    file_ = ROOT.TFile(fileName)
    c1 = file_.Get("c2")
    list_ = c1.GetListOfPrimitives()[1].GetListOfPrimitives()
    stack = list_[1]
    background = stack.GetStack().Last().Clone("background")
    signal = list_[3]
    roc = getROC(background,signal)
    c2 = ROOT.TCanvas()
    c2.SetGridx()
    c2.SetGridy()
    roc.Draw("APL")
    newFileName = fileName.replace(".root","_ROC.root")
    c2.SaveAs(newFileName)
    c2.SaveAs(newFileName.replace(".root",".png"))

if __name__ == "__main__":
    ROOT.gROOT.SetBatch()
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
    '''
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


