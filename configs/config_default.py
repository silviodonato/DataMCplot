import ROOT
from Classes import DatasetMCClass,DatasetDataClass,GroupClass,HistogramClass

## User C++ function to be used in ROOT
userFunctions = [] #["functions.C"]

## Define the histograms to be plotted
cut = "Sum$(jets_pt)>600"
histoTemplate = HistogramClass(
    var = "jets_pt[0]",
    nbins = 20, 
    xmin = 0, 
    xmax = 1000, 
    folder = "myPlotFolder", 
    weightMC = "puWeight", 
    cutsMC = cut, 
    cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v",
#    xTitle="", 
#    yTitle="", 
#    plotName=""
    )
histos = []
## If var is a string, the plot will be obtained using the TTree::Draw function (very fast)
histos.append(histoTemplate.clone( var="jets_pt[0]" ) )
histos.append(histoTemplate.clone( var="jets_pt[1]" ) )

## If var is a function, the plot will be obtained using looping over the tree
def myFuction(tree):
    value = tree.jets_pt[0] - tree.jets_pt[1]
    return value
histos.append(histoTemplate.clone( var=myFuction , nbins=100, xmin=0, xmax=500, xTitle="myFuction"))


## Define the datasets, ie. ROOT files with a cross-section (for MC) or integrated lumi (for data)
br_h_to_bb = 0.577
xsec_tth = 0.5085
#xsection is from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV

prefix = "Oct19/Oct19-__"
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
        lumi = 19786,
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
