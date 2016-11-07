import ROOT
from Classes import DatasetMCClass,DatasetDataClass,GroupClass,HistogramClass

'''
HLT_BIT_HLT_PFHT450_SixJet40_v
HLT_BIT_HLT_PFHT400_SixJet30_v
HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v
HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v
'''

## User C++ function to be used in ROOT
userFunctions = ["functions.C"]

## Define the histograms to be plotted
#cut = "Max$(jets_btagCSV)>0.8"
#cut = "leps_pt[0]>25 && abs(leps_pdgId[0])==13 && Sum$(jets_pt>0)>=6 && jets_pt[3]>60"
cut = "is_sl & leps_pt[0]>60 && abs(leps_pdgId[0])==11 && Sum$(jets_pt>0)>=6 && met_pt>60 && jets_pt[3]>60"

#triggerWeight = "trigger450(ht, Alt$(jets_pt[5],0), Max$(jets_btagCSV))/0.635423"
#triggerWeight = "0.3"
triggerWeight = "trigger450(ht, Alt$(jets_pt[5],0))"
triggerWeight = "0.55"
triggerWeight = "trigger400(ht, Alt$(jets_pt[5],0))"
histos = []
dataPreselection =  "&& (HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v) && run<276811"

########################### denominator ####################################################
triggerWeight = "trigger450(ht, Alt$(jets_pt[5],0))"
histoTemplate = HistogramClass(
    var = "jets_pt[0]",
    nbins = 50, 
    xmin = 0, 
    xmax = 1000, 
    folder = "checkSingleElectron", 
    weightMC = "max(0,puWeight*(1+2.5*(puWeightDown-puWeight)/puWeight)) * btagWeightCMVAV2 * "+triggerWeight, 
    cutsMC = cut, 
    cutsData = cut + dataPreselection,
    )

histos.append(histoTemplate.clone( var="Max$(jets_btagCMVA)", nbins = 50, xmin = -1, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCMVA,1,Iteration$,Length$))", nbins = 50, xmin = -1, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCMVA,2,Iteration$,Length$))", nbins = 50, xmin = -1, xmax = 1 ))
histos.append(histoTemplate.clone( var="ht", nbins = 50, xmin = 0, xmax = 2000 ))
histos.append(histoTemplate.clone( var="Alt$(jets_pt[5])", nbins = 50, xmin = 0, xmax = 120 ))

## Define the datasets, ie. ROOT files with a cross-section (for MC) or integrated lumi (for data)
br_h_to_bb = 0.577
xsec_tth = 0.5085
#xsection is from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV

prefix = "Nov3/Oct19-__"
datasetMC = {
    "tt" : DatasetMCClass(
        xsec = 831.76,
        fileName = prefix+"TT_TuneCUETP8M1_13TeV-powheg-pythia8.root",
    ),
    "tth" : DatasetMCClass(
        xsec = xsec_tth * br_h_to_bb,
        fileName = prefix+"ttHTobb_M125_13TeV_powheg_pythia8.root",
    ),
    "tthnobb" : DatasetMCClass(
        xsec = xsec_tth * (1.-br_h_to_bb),
        fileName = prefix+"ttHTobb_M125_13TeV_powheg_pythia8.root",
    ),
    "qcd300" : DatasetMCClass(
        xsec = 366800.0,
        fileName = prefix+"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd500" : DatasetMCClass(
        xsec = 29370.0,
        fileName = prefix+"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd700" : DatasetMCClass(
        xsec = 6524.0,
        fileName = prefix+"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd1000" : DatasetMCClass(
        xsec = 1064.0,
        fileName = prefix+"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd1500" : DatasetMCClass(
        xsec = 121.5,
        fileName = prefix+"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd2000" : DatasetMCClass(
        xsec = 25.42,
        fileName = prefix+"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
}
datasetData = {
    "JetHT" : DatasetDataClass(
        lumi = 5000,
        fileName = prefix+"JetHT.root"
    ),
}

