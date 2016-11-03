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
triggerWeight = "0.75"
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

#histos.append(histoTemplate.clone( var="jets_pt[3]", xmin = 0, xmax = 250 ))

#histos.append(histoTemplate.clone( var="leps_pt[0]", xmin = 0, xmax = 200 ))
#histos.append(histoTemplate.clone( var="transverseMass(met_pt, met_phi, leps_pt[0], leps_phi[0])", xmin = 0, xmax = 250 ))
#histos.append(histoTemplate.clone( var="met_pt", xmin = 0, xmax = 250 ))
#histos.append(histoTemplate.clone( var="nPVs", xmin = 0, xmax = 40 ))
#histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)", xmin = 0, xmax = 1 ))

histos.append(histoTemplate.clone( var="Max$(jets_btagCMVA)", xmin = -1, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCMVA,1,Iteration$,Length$))", nbins = 20, xmin = -1, xmax = 1 ))
histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCMVA,2,Iteration$,Length$))", nbins = 20, xmin = -1, xmax = 1 ))

#histos.append(histoTemplate.clone( var="Max$(jets_btagCSVNoHipMitigation)", xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))", nbins = 20, xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="Sum$(CSVn(jets_btagCSV,2,Iteration$,Length$))", nbins = 20, xmin = 0, xmax = 1 ))
#histos.append(histoTemplate.clone( var="ht", xmin = 0, xmax = 2000 ))
#histos.append(histoTemplate.clone( var="Alt$(jets_pt[5],0)", xmin = 0, xmax = 120 ))
##histos.append(histoTemplate.clone( var="Wmass", xmin = 0, xmax = 250 ))
##histos.append(histoTemplate.clone( var="met_pt", xmin = 0, xmax = 250 ))

## Define the datasets, ie. ROOT files with a cross-section (for MC) or integrated lumi (for data)
br_h_to_bb = 0.577
xsec_tth = 0.5085
#xsection is from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV

prefix = "Nov3_lept/Oct19-__"
datasetMC = {
    "tt" : DatasetMCClass(
        xsec = 831.76,
        fileName = prefix+"TT_TuneCUETP8M1_13TeV-powheg-pythia8.root",
    ),
}
datasetData = {
    "SingleElectron" : DatasetDataClass(
        lumi = 12900,
#        lumi = 19000,
        fileName = prefix+"SingleElectron.root"
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
        samples = ["SingleElectron"]
    ),
]
