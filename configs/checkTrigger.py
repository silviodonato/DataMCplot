import ROOT
from Classes import DatasetMCClass,DatasetDataClass,GroupClass,HistogramClass

## User C++ function to be used in ROOT
userFunctions = ["functions.C"]

## Define the histograms to be plotted
cut = "Alt$(jets_pt[5],0)>40"
#triggerWeight = "trigger450(ht, Alt$(jets_pt[5],0), Max$(jets_btagCSV))/0.635423"
#triggerWeight = "0.3"
triggerWeight = "trigger450(ht, Alt$(jets_pt[5],0))"
triggerWeight = "0.55"
triggerWeight = "trigger400(ht, Alt$(jets_pt[5],0))"
histoTemplate = HistogramClass(
    var = "jets_pt[0]",
    nbins = 1000, 
    xmin = 0, 
    xmax = 1000, 
    folder = "checkTrigger400", 
    weightMC = "1. * puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight, 
    cutsMC = cut, 
#    cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v",
#    cutsData = cut + "&&HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v",
    cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_v",
#    cutsData = cut + "&&HLT_BIT_HLT_PFHT450_SixJet40_v",
#    xTitle="", 
#    yTitle="", 
#    plotName=""
    normalized = False,
    )

histos = []

cut = "Alt$(jets_pt[5],0)>40"
histoTemplate.cutsMC = cut 


################# normalization ##################################
cut = "Alt$(jets_pt[6],0)>60 && ht>600"
histoTemplate.folder = "checkTrigger400"
histoTemplate.cutsMC = cut 
histoTemplate.cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_v ",
triggerWeight = "0.190696"
histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight 
histoTemplate.plotName = "normalization" 
histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))

###################################################
histoTemplate.plotName = "" 
cut = "Alt$(jets_pt[5],0)>40"
histoTemplate.folder = "checkTrigger450"
#histoTemplate.cutsData = cut + "&&HLT_BIT_HLT_PFHT450_SixJet40_v",
histoTemplate.cutsMC = cut 
histoTemplate.cutsData = cut + "&&HLT_BIT_HLT_PFHT450_SixJet40_v ",
triggerWeight = "0.577103 * trigger450(Sum$(jets_pt*(jets_pt>40)), Alt$(jets_pt[5],0))"
#triggerWeight = "1"
histoTemplate.weightMC = "puWeightICHEP450(puWeight,puWeightDown) *"+triggerWeight 
histos.append(histoTemplate.clone( var="Alt$(jets_pt[5],0)", xmin = 0, xmax = 120 ))
histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))
histos.append(histoTemplate.clone( var="nPVs", xmin = 0, xmax = 40 ))
histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))", xmin = 0, xmax = 1 ))

###########################################
### If var is a string, the plot will be obtained using the TTree::Draw function (very fast)
histoTemplate.folder = "checkTrigger400"
histoTemplate.cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_v",
triggerWeight = "0.190696 * trigger400(ht, Alt$(jets_pt[5],0))"
histoTemplate.weightMC = "puWeightICHEP400(puWeight,puWeightDown) *"+triggerWeight
histos.append(histoTemplate.clone( var="Alt$(jets_pt[5],0)", xmin = 0, xmax = 120 ))
histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))
histos.append(histoTemplate.clone( var="nPVs", xmin = 0, xmax = 40 ))
histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))", xmin = 0, xmax = 1 ))

#####################################################

histoTemplate.folder = "checkTriggerCSV450"
histoTemplate.cutsData = cut + "&&HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v",
triggerWeight = "triggerCSV450(Sum$(jets_pt*(jets_pt>40)), Alt$(jets_pt[5],0), Max$(jets_btagCSV) )"
histoTemplate.weightMC = "puWeightICHEP(puWeight,puWeightDown) *"+triggerWeight 
#histos.append(histoTemplate.clone( var="nPVs", xmin = 0, xmax = 40 ))
histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))
histos.append(histoTemplate.clone( var="Alt$(jets_pt[5],0)", xmin = 0, xmax = 120 ))

#####################################################

histoTemplate.folder = "checkTriggerCSV400"
histoTemplate.cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v",
triggerWeight = "triggerCSV400(ht, Alt$(jets_pt[5],0), Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$)))"
histoTemplate.weightMC = "puWeightICHEP(puWeight,puWeightDown) *"+triggerWeight 
histos.append(histoTemplate.clone( var="nPVs", xmin = 0, xmax = 40 ))
histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))
histos.append(histoTemplate.clone( var="Alt$(jets_pt[5],0)", xmin = 0, xmax = 120 ))

#####################################################

histoTemplate.folder = "checkTriggerCSV450_and_CSV400"
histoTemplate.cutsMC = cut 
histoTemplate.cutsData = cut + "&&(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v && HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v)",
triggerWeight = "triggerCSV450_and_CSV400(Sum$(jets_pt*(jets_pt>40)), Alt$(jets_pt[5],0),Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$)))"
histoTemplate.weightMC = "puWeightICHEP(puWeight,puWeightDown) *"+triggerWeight 
histos.append(histoTemplate.clone( var="nPVs", xmin = 0, xmax = 40 ))
histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))
histos.append(histoTemplate.clone( var="Alt$(jets_pt[5],0)", xmin = 0, xmax = 120 ))

#####################################################

histoTemplate.folder = "checkTriggerCSV450_or_CSV400"
histoTemplate.cutsMC = cut 
histoTemplate.cutsData = cut + "&&(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v||HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v)",
triggerWeight = "triggerCSV450_or_CSV400(ht, Sum$(jets_pt*(jets_pt>40)), Alt$(jets_pt[5],0), Max$(jets_btagCSV), Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$)))"
histoTemplate.weightMC = "puWeightICHEP(puWeight,puWeightDown) *"+triggerWeight 
histos.append(histoTemplate.clone( var="nPVs", xmin = 0, xmax = 40 ))
histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))
histos.append(histoTemplate.clone( var="Alt$(jets_pt[5],0)", xmin = 0, xmax = 120 ))

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
