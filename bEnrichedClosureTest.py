from glob import glob
import ROOT
import array
import os,sys

ROOT.gStyle.SetOptStat(0)

cut = "1"
var  = "btag_LR_4b_3b_btagCSV >> histo(40,0,1)"
#var  = "ht >> histo(50,0,1000)"

c1 = ROOT.TCanvas("c1","")

for HT in ["HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000"]:
    BGenFilter_fn = "Apr27/QCD_%s_BGenFilter_merged.root"%HT
    inclusive_fn  = "Apr27/QCD_%s_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"%HT
    bEnriched_fn  = "Apr27/QCD_%s_bEnriched_merged.root"%HT
    noB_fn  = "Apr27/QCD_%s_NoB.root"%HT

    BGenFilter_file = ROOT.TFile(BGenFilter_fn)
    inclusive_file = ROOT.TFile(inclusive_fn)
    bEnriched_file = ROOT.TFile(bEnriched_fn)
    noB_file = ROOT.TFile(noB_fn)

    BGenFilter = BGenFilter_file.Get("tree")
    inclusive = inclusive_file.Get("tree")
    bEnriched = bEnriched_file.Get("tree")
    noB = noB_file.Get("tree")

    BGenFilter_count = BGenFilter_file.Get("CountWeighted").GetBinContent(1)
    inclusive_count = inclusive_file.Get("CountWeighted").GetBinContent(1)
    bEnriched_count = bEnriched_file.Get("CountWeighted").GetBinContent(1)
    noB_count = noB_file.Get("CountWeighted").GetBinContent(1)
    
    BGenFilter.Draw(var,cut)
    BGenFilter_histo = ROOT.gDirectory.Get("histo").Clone("BGenFilter_histo")
    BGenFilter_histo.Scale(1./BGenFilter_count)
    
    inclusive.Draw(var,cut)
    inclusive_histo = ROOT.gDirectory.Get("histo").Clone("inclusive_histo")
    inclusive_histo.Scale(1./inclusive_count)
    
    bEnriched.Draw(var,cut)
    bEnriched_histo = ROOT.gDirectory.Get("histo").Clone("bEnriched_histo")
    bEnriched_histo.Scale(1./bEnriched_count)
    
    noB.Draw(var,cut)
    noB_histo = ROOT.gDirectory.Get("histo").Clone("noB_histo")
    noB_histo.Scale(1./noB_count)
    
    inclusive_histo.SetLineColor(ROOT.kBlack)
    BGenFilter_histo.SetLineColor(ROOT.kGreen)
    bEnriched_histo.SetLineColor(ROOT.kRed)
    noB_histo.SetLineColor(ROOT.kBlue)
    
    inclusive_histo.SetLineWidth(2)
    
    inclusive_histo.SetFillColor(inclusive_histo.GetLineColor())
    BGenFilter_histo.SetFillColor(BGenFilter_histo.GetLineColor())
    bEnriched_histo.SetFillColor(bEnriched_histo.GetLineColor())
    noB_histo.SetFillColor(noB_histo.GetLineColor())
    
    BGenFilter_histo.Add(noB_histo)
    BGenFilter_histo.Add(bEnriched_histo)
    BGenFilter_histo.SetMaximum(1.3*BGenFilter_histo.GetMaximum())
    BGenFilter_histo.SetLineColor(ROOT.kGreen+2)
    BGenFilter_histo.Draw("ERR,HIST")

    bEnriched_histo.Add(noB_histo)
    bEnriched_histo.Draw("HIST,same")
    
    noB_histo.Draw("HIST,same")
    
    inclusive_histo.Draw("same")
    
    c1.SaveAs("bEnrichedCheck%s.png"%HT)
    

