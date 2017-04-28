from glob import glob
import ROOT
import array
import os,sys


BGenFilter_cut = "lheNb==0 && nGenStatus2bHad>0"
bEnriched_cut  = "lheNb>0"

for HT in ["HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000"]:
    BGenFilter_fn = "Apr27/QCD_%s_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"%HT
    inclusive_fn  = "Apr27/QCD_%s_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"%HT
    bEnriched_fn  = "Apr27/QCD_bEnriched_%s_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"%HT

    BGenFilter_file = ROOT.TFile(BGenFilter_fn)
    inclusive_file = ROOT.TFile(inclusive_fn)
    bEnriched_file = ROOT.TFile(bEnriched_fn)

    BGenFilter = BGenFilter_file.Get("tree")
    inclusive = inclusive_file.Get("tree")
    bEnriched = bEnriched_file.Get("tree")

    BGenFilter_count = BGenFilter_file.Get("CountWeighted").GetBinContent(1)
    inclusive_count = inclusive_file.Get("CountWeighted").GetBinContent(1)
    bEnriched_count = bEnriched_file.Get("CountWeighted").GetBinContent(1)

    print "------------------"
    print HT
    print "------------------"
    print "BGenFilter region"
    print "inclusive: ",inclusive.Draw("",BGenFilter_cut)
    print "enriched: ",BGenFilter.Draw("","")
    print "improvement (%): ",100.*BGenFilter.Draw("","")/inclusive.Draw("",BGenFilter_cut)
    print "------------------"
    print "bEnriched region"
    print "inclusive: ",inclusive.Draw("",bEnriched_cut)
    print "enriched: ",bEnriched.Draw("","")
    print "improvement (%): ",100.*bEnriched.Draw("","")/inclusive.Draw("",bEnriched_cut)

