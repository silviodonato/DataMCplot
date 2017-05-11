from glob import glob
import ROOT
import array
import os,sys

ROOT.gStyle.SetOptStat(0)

cut = "1"
var  = "(mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))**0.2 >> histo(10,0.,1)"
#var  = "btag_LR_4b_3b_btagCSV >> histo(30,0.75,1)"


#QGL_high = "&& qg_LR_4b_flavour_4q_0q>0.7"
#QGL_low = "&& qg_LR_4b_flavour_4q_0q<0.7"

QGL_high = "&& 1"
QGL_low = "&& 1"



#BTag_high = "&& nBCSVM>=3 && btag_LR_4b_2b_btagCSV>0.996 "
#BTag_low = "&& nBCSVM>=3 && btag_LR_4b_2b_btagCSV>0.9 && btag_LR_4b_2b_btagCSV<0.95"

BTag_high = "&& nBCSVM==4"
BTag_low = "&& nBCSVM==3 && Sum$(jets_btagCSV>0.5426)==4"

regSR = "(cat==8 || cat==9) && mem_tth_FH_4w2h2t_p>0" + QGL_high + BTag_high
regVR = "(cat==8 || cat==9) && mem_tth_FH_4w2h2t_p>0" + QGL_low + BTag_high
regCR = "(cat==8 || cat==9) && mem_tth_FH_4w2h2t_p>0" + QGL_high + BTag_low
regCR2 = "(cat==8 || cat==9) && mem_tth_FH_4w2h2t_p>0" + QGL_low + BTag_low

#regSR = "(cat==8 || cat==9) && qg_LR_4b_flavour_4q_0q>0.7 && mem_tth_FH_4w2h2t_p>0"
#regVR = "(cat==8 || cat==9) && qg_LR_4b_flavour_4q_0q<0.7 && mem_tth_FH_4w2h2t_p>0"

#regSR = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/mem_ttbb_FH_4w2h2t_p)>0.02"
#regVR = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/mem_ttbb_FH_4w2h2t_p)<0.02"

#regVR = ""
#regCR = ""

#var  = "ht >> histo(50,0,1000)"
#SR 4b: btag_LR_4b_2b_btagCSV>0.99
#VR 4b: btag_LR_4b_2b_btagCSV>0.75 && btag_LR_4b_2b_btagCSV<0.88

c1 = ROOT.TCanvas("c1","")

#for HT in ["HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000"]:
HT = "test"
#if True:
#for HT in ["HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000","HT2000toInf","TT","data"]:
#for HT in ["TT"]:
#for HT in ["QCD"]:
for HT in ["HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000","HT2000toInf","TT"]:
    inclusive_fn  = "Apr27/QCD_%s_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"%HT
    if "TT" in HT: inclusive_fn  = "Apr27/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root"
    if "signal" in HT: inclusive_fn  = "Apr27/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root"
    if "data" in HT: inclusive_fn  = "Apr27/JetHT.root"
#    inclusive = ROOT.TChain("tree")
#    inclusive.Add("Apr27/QCD_*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
    
    inclusive_file = ROOT.TFile(inclusive_fn)
    inclusive = inclusive_file.Get("tree")

    inclusive.Draw(var,regSR)
    histoSR = ROOT.gDirectory.Get("histo").Clone("histoSR")
    
    inclusive.Draw(var,regVR)
    histoVR = ROOT.gDirectory.Get("histo").Clone("histoVR")
    
    inclusive.Draw(var,regCR)
    histoCR = ROOT.gDirectory.Get("histo").Clone("histoCR")
    
    inclusive.Draw(var,regCR2)
    histoCR2 = ROOT.gDirectory.Get("histo").Clone("histoCR2")
    
    histoExp = histoSR.Clone("histoExp1")
    histoExp.Reset()
    
    for i in range(histoExp.GetXaxis().GetNbins()):
        cr = histoCR.GetBinContent(i)
        cr2 = histoCR2.GetBinContent(i)
        vr = histoVR.GetBinContent(i)
        if cr2>0:
            histoExp.SetBinContent(i,vr*cr/cr2)
    
    if "data" in HT: histoSR.Reset()
    
    histoSR.SetLineColor(ROOT.kBlue)
    histoVR.SetLineColor(ROOT.kRed)
    histoCR.SetLineColor(ROOT.kGreen)
    histoCR2.SetLineColor(ROOT.kBlack)
    histoExp.SetLineColor(ROOT.kRed)
    
    histoSR.SetLineWidth(2)
    histoVR.SetLineWidth(2)
    histoCR.SetLineWidth(2)
    histoCR2.SetLineWidth(2)
    histoExp.SetLineWidth(2)
    
    histoSR.SetMaximum(1.2*max(histoSR.GetMaximum(),histoExp.GetMaximum()))
    histoSR.Draw("ERR")
    histoExp.Draw("ERR,same")
    
    c1.SaveAs("ddExp%s.png"%HT)
    
    if histoSR.Integral()>0:
        histoSR.Scale(1./histoSR.Integral())
    histoVR.Scale(1./histoVR.Integral())
    histoCR.Scale(1./histoCR.Integral())
    histoCR2.Scale(1./histoCR2.Integral())
    
    histoSR.SetMaximum(1.2*max(histoSR.GetMaximum(),histoVR.GetMaximum()))
    histoVR.SetMaximum(1.2*max(histoCR2.GetMaximum(),histoVR.GetMaximum()))
    histoVR.Draw()
    histoCR2.Draw("same")
    c1.SaveAs("ddCheckVR%s.png"%HT)
    histoSR.Draw()
    histoCR.Draw("same")
    c1.SaveAs("ddCheckSR%s.png"%HT)
    
    
#    ratio = histoSR.Clone("ratio")
#    ratio.Divide(histoSR,histoCR2)
#    ratio.SetMaximum(2)
#    ratio.SetMinimum(0.01)
#    ratio.Draw()
#    
#    c1.SaveAs("ddCheckRatio%s.png"%HT)
    
#    var2D = "(mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))**0.2:btag_LR_4b_2b_btagCSV"
#    c1.SetLogz()
#    inclusive.Draw(var2D,"cat==9 && mem_tth_FH_4w2h2t_p>0","COLZ")
#    inclusive.Draw(var2D,"cat==9 && mem_tth_FH_4w2h2t_p>0","prof,same")
#    
#    c1.SaveAs("ddCheck2D%s.png"%HT)

