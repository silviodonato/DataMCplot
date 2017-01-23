'''
FH_3w2h2t 7j4b
FH_1w1w2h2t 8j4b, 9j4b
FH_4w2h1t 7j,3b, 8j,3b, 9j,3b


Wmass cuts: 
cat7: njets=7, Wmass [60,100]   mem_ttbb_FH_3w2h2t_p    mem_ttbb_FH_4w2h1t_p
cat8: njets=8, Wmass [60,100]   mem_ttbb_FH_1w1w2h2t_p  mem_ttbb_FH_4w2h1t_p
cat9: njets=9, Wmass [72,94]    mem_ttbb_FH_1w1w2h2t_p  mem_ttbb_FH_4w2h1t_p

(Wmass>60&&Wmass<100)
(Wmass>72&&Wmass<94)


SR 4b: btag_LR_4b_2b_btagCSV>0.99
CR 4b: btag_LR_4b_2b_btagCSV>0.75 && btag_LR_4b_2b_btagCSV<0.88

SR 3b: btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.83
CR 3b: btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.60 && btag_LR_3b_2b_btagCSV<0.80

    A3 = 0.83
    B3 = 0.6
    C3 = 0.8

'''
import ROOT
from Classes import DatasetMCClass,DatasetDataClass,DatasetDataDrivenClass,GroupClass,HistogramClass
from addPlots import addPlots

## User C++ function to be used in ROOT
userFunctions = ["functions.C"]

## Define the histograms to be plotted
cut = "jets_pt[5]>50 && ht40>600 && Sum$(jets_btagCSV>0.8)>=2" # && (!std::isnan(puWeightICHEP))
weights = "qgWeight*0.92*(btagWeightCSV*(ngenTopHad>0)+1.*(ngenTopHad==0))"

histoTemplate = HistogramClass()
histos = []

####################################  inclusive plots #########################

category = "inclusive"

histoTemplate.cutsMC = cut
histoTemplate.cutsData = cut + "&&(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v||HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v)"
histoTemplate.weightMC = weights

histoTemplate.folder = "plots_mcQCD_%s"%category

addPlots(histos, histoTemplate, category) 

#################################

category = "inclusiveQGLR"

qgLRRegion = " && Sum$(jets_pt<30)==0"
histoTemplate.cutsMC = cut + qgLRRegion
histoTemplate.cutsData = cut + qgLRRegion + "&&(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v||HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v)"
histoTemplate.weightMC = weights

histoTemplate.folder = "plots_mcQCD_%s"%category

addPlots(histos, histoTemplate, category) 

################################ Loop on the regions #########################################################

cut4b_SR = "(btag_LR_4b_2b_btagCSV>0.99)"
cut3b_SR = "(btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.83)"

cut4b_CR = "(btag_LR_4b_2b_btagCSV>0.75 && btag_LR_4b_2b_btagCSV<0.88)"
cut3b_CR = "(btag_LR_4b_2b_btagCSV<0.99 && btag_LR_3b_2b_btagCSV>0.60 && btag_LR_3b_2b_btagCSV<0.80)"

for region in ["SR","VR","CR","CR2"]:
    if region in ["SR","VR"]:
        cut3b = cut3b_SR
        cut4b = cut4b_SR
    elif region in ["CR","CR2"]:
        cut3b = cut3b_CR
        cut4b = cut4b_CR
    
    if region in ["SR","CR"]:
        cutRegion = " Sum$(jets_pt<30)==0 && qg_LR_4b_flavour_4q_0q>0.5"
    elif region in ["VR","CR2"]:
        cutRegion = " Sum$(jets_pt<30)==0 && qg_LR_4b_flavour_4q_0q<0.5"
    else:
        raise Exception("Region '%s' unknown!"%region)
    
    if region is "SR":
        histoTemplate.blinded = True
    else:
        histoTemplate.blinded = False
    
    for njet in ["7j","8j","9j"]:
        for nbjet in ["3b","4b"]:
            category = "mcQCDcatQGL_%s_"%region+njet+nbjet
            cutCategory = ""
            if njet is "7j":
                cutCategory += " && njets==7"
                cutCategory += " && Wmass>60 && Wmass<100"
            elif njet is "8j":
                cutCategory += " && njets==8"
                cutCategory += " && Wmass>60 && Wmass<100"
            elif njet is "9j":
                cutCategory += " && njets==9"
                cutCategory += " && Wmass>72 && Wmass<94"
            else:
                raise Exception("Category(njet) '%s' unknown!"%njet)
            
            if nbjet is "3b":
                cutCategory += " && "+cut3b
            elif nbjet is "4b":
                cutCategory += " && "+cut4b
            else:
                raise Exception("Category(nbjet) '%s' unknown!"%nbjet)
            
            histoTemplate.cutsMC = cut + " && " + cutRegion + cutCategory
            histoTemplate.cutsData = cut + " && " + cutRegion + cutCategory + "&&(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v||HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v)"
            histoTemplate.weightMC = weights
            
            histoTemplate.folder = "plots_%s"%category
            histoTemplate.region = region
            histoTemplate.category = njet+nbjet
            
            addPlots(histos, histoTemplate, category)
            
##########################################################################################################

## Define the datasets, ie. ROOT files with a cross-section (for MC) or integrated lumi (for data)
br_h_to_bb = 0.577
xsec_tth = 0.5085
#xsection is from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV

#QCD_SF = 0.7404*1.0755157675741747
QCD_SF = 0.778
QCD_SF = 0.755

prefix = "Jan16/Dec24__"
prefixJan6 = "Jan16/Jan6__"
datasets = {
    "tt" : DatasetMCClass(
        xsec = 831.76,
        fileName = prefixJan6+"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",
    ),
    "tth" : DatasetMCClass(
        xsec = xsec_tth * br_h_to_bb,
        fileName = prefix+"ttHTobb_M125_13TeV_powheg_pythia8.root",
    ),
#    "tthnobb" : DatasetMCClass(
#        xsec = xsec_tth * (1.-br_h_to_bb),
#        fileName = prefix+"ttHTobb_M125_13TeV_powheg_pythia8.root",
#    ),
    "qcd300" : DatasetMCClass(
        xsec = QCD_SF * 366800.0 * 0.166308, ## 0.166308 is to fix the issue with the Count (empty tree do no contribute to Count!)
        fileName = prefix+"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd500" : DatasetMCClass(
        xsec = QCD_SF * 29370.0,
        fileName = prefix+"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd700" : DatasetMCClass(
        xsec = QCD_SF * 6524.0,
        fileName = prefix+"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd1000" : DatasetMCClass(
        xsec = QCD_SF * 1064.0,
        fileName = prefix+"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd1500" : DatasetMCClass(
        xsec = QCD_SF * 121.5,
        fileName = prefix+"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd2000" : DatasetMCClass(
        xsec = QCD_SF * 25.42,
        fileName = prefix+"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    
#    "qcdDataDriven" : DatasetDataDrivenClass(
#        weight = "qcdWeight * 1.",
#        fileName = prefixJan6+"QCDDataDriven.root"
#    ),
    
    "JetHT" : DatasetDataClass(
        lumi = 10593.875,
        fileName = prefixJan6+"JetHT.root"
    ),
}

## Define the groups, ie. sets of datasets, with a latexName name and a color
groups =[
    GroupClass(
        color = ROOT.kGreen,
        latexName = "mc QCD",
        samples = ["qcd300","qcd500","qcd700","qcd1000","qcd1500","qcd2000"],
#        samples = ["qcd500","qcd700","qcd1000","qcd1500","qcd2000"], #"qcd300",
        groupType = "background"
    ),
#    GroupClass(
#        color = ROOT.kGreen,
#        latexName = "d.d.QCD",
#        samples = ["qcdDataDriven"],
#        groupType = "backgroundFromData"
#    ),
    GroupClass(
        color = ROOT.kRed,
        latexName = "t#bar{t}",
        samples = ["tt"],
        groupType = "background"
    ),
    GroupClass(
        color = ROOT.kBlue,
        latexName = "signal",
#        samples = ["tth","tthnobb"]
        samples = ["tth"],
        groupType = "signal"
    ),
    GroupClass(
        color = ROOT.kBlack,
        latexName = "Data",
        samples = ["JetHT"],
        groupType = "data"
    ),
]
