import ROOT
from Classes import DatasetMCClass,DatasetDataClass,GroupClass,HistogramClass

## User C++ function to be used in ROOT
userFunctions = ["functions.C"]

## Define the histograms to be plotted
cut = "Alt$(jets_pt[5],0)>60 && ht>500"
triggerWeight = "0.190696"
histoTemplate = HistogramClass(
    var = "jets_pt[0]",
    nbins = 1000, 
    xmin = 0, 
    xmax = 1000, 
    folder = "checkWeights", 
    weightMC = "1.*"+triggerWeight, 
    cutsMC = cut, 
    cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_v",
#    plotName=""
    normalized = False,
    )

histos = []



###################################################
histoTemplate.weightMC = "1. *"+triggerWeight 
histoTemplate.xTitle = ""
histoTemplate.var = "nPVs"
histoTemplate.nbins, histoTemplate.xmin, histoTemplate.xmax  = 60, 0, 60
histoTemplate.plotName = "nPVs_noWeights"

histos.append(histoTemplate.clone())

histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight 
histoTemplate.plotName = "nPVs"
histos.append(histoTemplate.clone())

histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight 
histoTemplate.var = "ht"
histoTemplate.nbins, histoTemplate.xmin, histoTemplate.xmax  = 200, 0, 2000
histoTemplate.plotName = "ht_noWeights"
histos.append(histoTemplate.clone())

triggerWeight = "0.190696 * trigger400(ht,Alt$(jets_pt[5],0))"
histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight 
histoTemplate.var = "ht"
histoTemplate.plotName = "ht"
histos.append(histoTemplate.clone())

histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight 
histoTemplate.var = "Max$(jets_btagCSV)"
histoTemplate.nbins, histoTemplate.xmin, histoTemplate.xmax  = 200, 0, 1
histoTemplate.plotName = "csv1_noWeight"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))"
histoTemplate.plotName = "csv2_noWeight"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_btagCSV,2,Iteration$,Length$))"
histoTemplate.plotName = "csv3_noWeight"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_btagCSV,3,Iteration$,Length$))"
histoTemplate.plotName = "csv4_noWeight"
histos.append(histoTemplate.clone())

histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) * btagWeightCSV * "+triggerWeight 
histoTemplate.var = "Max$(jets_btagCSV)"
histoTemplate.plotName = "csv1"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))"
histoTemplate.plotName = "csv2"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_btagCSV,2,Iteration$,Length$))"
histoTemplate.plotName = "csv3"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_btagCSV,3,Iteration$,Length$))"
histoTemplate.plotName = "csv4"
histos.append(histoTemplate.clone())

histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight 
(histoTemplate.nbins, histoTemplate.xmin, histoTemplate.xmax)  = (200, 0, 1)

histoTemplate.var = "Sum$(CSVn(jets_qgl,1,Iteration$,Length$))"
histoTemplate.plotName = "qgl2_noWeight"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_qgl,2,Iteration$,Length$))"
histoTemplate.plotName = "qgl3_noWeight"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_qgl,3,Iteration$,Length$))"
histoTemplate.plotName = "qgl4_noWeight"
histos.append(histoTemplate.clone())

histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) * Sum$(product(qg_sf(jets_qgl, jets_mcFlavour),Iteration$,Length$)) * "+triggerWeight 
(histoTemplate.nbins, histoTemplate.xmin, histoTemplate.xmax)  = (200, 0, 1)

histoTemplate.var = "Sum$(CSVn(jets_qgl,1,Iteration$,Length$))"
histoTemplate.plotName = "qgl2"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_qgl,2,Iteration$,Length$))"
histoTemplate.plotName = "qgl3"
histos.append(histoTemplate.clone())

histoTemplate.var = "Sum$(CSVn(jets_qgl,3,Iteration$,Length$))"
histoTemplate.plotName = "qgl4"
histos.append(histoTemplate.clone())


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
        lumi = 12900*0.868310518,
        fileName = prefix+"JetHT.root"
    ),
}

## Define the groups, ie. sets of datasets, with a latexName name and a color
groups =[
    GroupClass(
        color = ROOT.kGreen,
        latexName = "QCD",
        samples = ["qcd300","qcd500","qcd700","qcd1000","qcd1500","qcd2000"]
    ),
    GroupClass(
        color = ROOT.kRed,
        latexName = "t#bar{t}",
        samples = ["tt"]
    ),
    GroupClass(
        color = ROOT.kBlue,
        latexName = "signal",
        samples = ["tth","tthnobb"]
    ),
    GroupClass(
        color = ROOT.kBlack,
        latexName = "Data",
        samples = ["JetHT"]
    ),
]
