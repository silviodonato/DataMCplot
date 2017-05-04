from glob import glob
import ROOT
import array
import os,sys

ROOT.gStyle.SetOptStat(0)

cut = "1"
var  = "(mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))**0.2 >> histo(10,0.,1)"
#var  = "btag_LR_4b_3b_btagCSV >> histo(30,0.75,1)"
reg1 = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))>0.000000003 && mem_tth_FH_4w2h2t_p>0 && btag_LR_4b_2b_btagCSV>0.99"
reg2 = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))>0.000000003 && mem_tth_FH_4w2h2t_p>0 && btag_LR_4b_2b_btagCSV>0.75 && btag_LR_4b_2b_btagCSV<0.88"
reg3 = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))>0.000000003 && mem_tth_FH_4w2h2t_p>0 && btag_LR_4b_2b_btagCSV>0.88 && btag_LR_4b_2b_btagCSV<0.95"
reg4 = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))>0.000000003 && mem_tth_FH_4w2h2t_p>0 && btag_LR_4b_2b_btagCSV>0.95 && btag_LR_4b_2b_btagCSV<0.99"

#reg1 = "(cat==8 || cat==9) && qg_LR_4b_flavour_4q_0q>0.7 && mem_tth_FH_4w2h2t_p>0"
#reg2 = "(cat==8 || cat==9) && qg_LR_4b_flavour_4q_0q<0.7 && mem_tth_FH_4w2h2t_p>0"

#reg1 = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/mem_ttbb_FH_4w2h2t_p)>0.02"
#reg2 = "(cat==8 || cat==9) && (mem_tth_FH_4w2h2t_p/mem_ttbb_FH_4w2h2t_p)<0.02"

#var  = "ht >> histo(50,0,1000)"
#SR 4b: btag_LR_4b_2b_btagCSV>0.99
#CR 4b: btag_LR_4b_2b_btagCSV>0.75 && btag_LR_4b_2b_btagCSV<0.88

c1 = ROOT.TCanvas("c1","")

#for HT in ["HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000"]:
HT = "test"
inclusive_fn  = "Apr27/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
if True:
    inclusive_file = ROOT.TFile(inclusive_fn)
    inclusive = inclusive_file.Get("tree")

    inclusive.Draw(var,reg1,"NORM")
    histo1 = ROOT.gDirectory.Get("histo").Clone("histo1")
    
    inclusive.Draw(var,reg2,"NORM")
    histo2 = ROOT.gDirectory.Get("histo").Clone("histo2")
    
    inclusive.Draw(var,reg3,"NORM")
    histo3 = ROOT.gDirectory.Get("histo").Clone("histo3")
    
    inclusive.Draw(var,reg4,"NORM")
    histo4 = ROOT.gDirectory.Get("histo").Clone("histo4")
    
    histo1.SetLineColor(ROOT.kBlue)
    histo2.SetLineColor(ROOT.kRed)
    histo3.SetLineColor(ROOT.kGreen)
    histo4.SetLineColor(ROOT.kBlack)
    
    histo1.SetLineWidth(2)
    histo2.SetLineWidth(2)
    histo3.SetLineWidth(2)
    histo4.SetLineWidth(2)
    
    histo1.SetMaximum(1.2*max(histo1.GetMaximum(),histo2.GetMaximum()))
    histo1.Draw()
    histo2.Draw("same")
    histo3.Draw("same")
    histo4.Draw("same")
    
    c1.SaveAs("ddCheck%s.png"%HT)
    
#    var2D = "(mem_tth_FH_4w2h2t_p/(mem_ttbb_FH_4w2h2t_p+mem_tth_FH_4w2h2t_p))**0.2:btag_LR_4b_2b_btagCSV"
#    c1.SetLogz()
#    inclusive.Draw(var2D,"cat==9 && mem_tth_FH_4w2h2t_p>0","COLZ")
#    inclusive.Draw(var2D,"cat==9 && mem_tth_FH_4w2h2t_p>0","prof,same")
#    
#    c1.SaveAs("ddCheck2D%s.png"%HT)

