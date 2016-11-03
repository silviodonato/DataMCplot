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
cut = "leps_pt[0]>25 && abs(leps_pdgId[0])==13 && Sum$(jets_pt>0)>=6 && jets_pt[3]>60"
#triggerWeight = "trigger450(ht, Alt$(jets_pt[5],0), Max$(jets_btagCSV))/0.635423"
#triggerWeight = "0.3"
triggerWeight = "trigger450(ht, Alt$(jets_pt[5],0))"
triggerWeight = "0.55"
triggerWeight = "trigger400(ht, Alt$(jets_pt[5],0))"
histos = []
dataPreselection =  "&& (HLT_BIT_HLT_IsoMu22_v||HLT_BIT_HLT_IsoTkMu22_v) && run<276811"

########################### denominator ####################################################
triggerWeight = "0.75"
histoTemplate = HistogramClass(
    var = "jets_pt[0]",
    nbins = 50, 
    xmin = 0, 
    xmax = 1000, 
    folder = "checkSingleMuon_qgl", 
    weightMC = "max(0,puWeight*(1+2.5*(puWeightDown-puWeight)/puWeight)) * btagWeightCSV * "+triggerWeight, 
    cutsMC = cut, 
    cutsData = cut + dataPreselection,
    )

#histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_qgl,3,Iteration$,Length$))", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="jets_qgl[0]", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="jets_qgl[1]", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="jets_qgl[2]", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="jets_qgl[3]", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="jets_qgl[4]", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="Max$(jets_qgl)", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="Min$(jets_qgl)", xmin = 0, xmax = 1 ))


histoTemplate.folder = "checkSingleMuon_qgl_reweighted2"
histoTemplate.weightMC = histoTemplate.weightMC + "* Sum$(product(qg_sf(jets_qgl, jets_mcFlavour),Iteration$,Length$))"

histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_qgl,3,Iteration$,Length$))", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="jets_qgl[0]", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="jets_qgl[1]", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="jets_qgl[2]", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="jets_qgl[3]", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="jets_qgl[4]", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Max$(jets_qgl)", xmin = 0, xmax = 1 ))
histos.append(histoTemplate.clone( var="Min$(jets_qgl)", xmin = 0, xmax = 1 ))




## Define the datasets, ie. ROOT files with a cross-section (for MC) or integrated lumi (for data)
br_h_to_bb = 0.577
xsec_tth = 0.5085
#xsection is from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV

#prefix = "SingleLepton/Oct19-__"
prefix = "Nov3_lept/Oct19-__"
datasetMC = {
    "tt" : DatasetMCClass(
        xsec = 831.76,
        fileName = prefix+"TT_TuneCUETP8M1_13TeV-powheg-pythia8.root",
    ),
}
datasetData = {
    "SingleMuon" : DatasetDataClass(
        lumi = 12900,
#        lumi = 19000,
        fileName = prefix+"SingleMuon.root"
    ),
}

## Define the groups, ie. sets of datasets, with a latexName name and a color
groups =[
    GroupClass(
        color = ROOT.kRed,
        latexName = "t#bar{t}",
        samples = ["tt"]
    ),
    GroupClass(
        color = ROOT.kBlack,
        latexName = "Data",
        samples = ["SingleMuon"]
    ),
]
