userFunctions = ["functions.C"] #["CSVn.C"]

import ROOT
from Classes import DatasetMCClass,DatasetDataClass,GroupClass,HistogramClass

''' For trigger
#triggerWeight = "(0.5+0.5*erf((jets_pt[5]-39.1116)/7.50695)+0.0618949) * (0.5+0.440825*erf((ht-448.58)/75.0045)-0.0455728)"
triggerWeight = "1"

cut = "ht>600 && Sum$(jets_pt>50)>=6"
histoTemplate = HistogramClass(
    var = "jets_pt[0]",
    nbins = 100, 
    xmin = 0, 
    xmax = 1000, 
    folder = "triggerTurnOn", 
    weightMC = "puWeight*(1+4*(puWeightDown-puWeight)/puWeight) * 0.4 * btagWeightCSV " + "*" + triggerWeight, 
    cutsMC = cut, 
    cutsData = "HLT_ttH_FH_prescaled && "+cut,
#    xTitle="", 
#    yTitle="", 
#    plotName=""
    )


histos = []

cut = "ht>800"
histos.append(histoTemplate.clone( var="jets_pt[5]" , nbins=100, xmin=0, xmax=100, cutsMC = cut, cutsData = "HLT_ttH_FH_prescaled && "+cut, plotName="pt6_num"))

cut = "Sum$(jets_pt>0)>=6"
histos.append(histoTemplate.clone( var="ht" , nbins=100, xmin=0, xmax=2000, cutsMC = cut, cutsData = "HLT_ttH_FH_prescaled && "+cut, plotName="htt_num"))

#histos.append(histoTemplate.clone( var="ht" , nbins=60, xmin=0, xmax=60, cutsMC = "Sum$(jets_pt>50)>=6", cutsData = "HLT_ttH_FH_prescaled && "+cutsMC))
#histos.append(histoTemplate.clone( var="Max$(jets_btagCSV)" , nbins=60, xmin=0, xmax=60, cutsMC = "ht>600", cutsData = "HLT_ttH_FH_prescaled && "+cutsMC))
histos.append(histoTemplate.clone( var="jets_pt[5]" , nbins=100, xmin=0, xmax=100, cutsMC = cut, cutsData = "HLT_ttH_FH_prescaled && "+cut, plotName="pt6_num"))

'''


#cut = "(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v || HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v) && (btag_LR_geq2b_leq1b_btagCSV>0.85) && (btag_LR_3b_2b_btagCSV>0.93) && qg_LR_3b_flavour_3q_0q>0"
cut = "(btag_LR_geq2b_leq1b_btagCSV>0.85) && (btag_LR_3b_2b_btagCSV>0.93) && qg_LR_3b_flavour_3q_0q>0"
#triggerWeight = "(0.5+0.5*erf((jets_pt[5]-39.1116)/7.50695)+0.0618949) * (0.5+0.440825*erf((ht-448.58)/75.0045)-0.0455728)"
triggerWeight = "1"

#cut = "ht>600 && Sum$(jets_pt>50)>=6"
histoTemplate = HistogramClass(
    var = "jets_pt[0]",
    nbins = 20, 
    xmin = 0, 
    xmax = 1, 
    folder = "test", 
    weightMC = "puWeight*(1+4*(puWeightDown-puWeight)/puWeight) * 0.4 * btagWeightCSV " + "*" + triggerWeight, 
    cutsMC = cut, 
    cutsData = cut + "&&HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v",
#    xTitle="", 
#    yTitle="", 
#    plotName=""
    )


histos = []

#histos.append(histoTemplate.clone( var="btag_LR_4b_2b_btagCSV" ) )
#histos.append(histoTemplate.clone( var="btag_LR_4b_3b_btagCSV" ) )
#histos.append(histoTemplate.clone( var="btag_LR_3b_2b_btagCSV" ) )
#histos.append(histoTemplate.clone( var="btag_LR_geq2b_leq1b_btagCSV" ) )

def testFunction(tree):
    jets = []
    for (pt,eta,phi,mass,csv) in zip(tree.jets_pt,tree.jets_eta,tree.jets_phi,tree.jets_mass,tree.jets_btagCSV):
#    for (pt,eta,phi,mass,csv) in zip(tree.jets_mcPt,tree.jets_mcEta,tree.jets_mcPhi,tree.jets_mcM,tree.jets_mcNumBHadrons):
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(pt,eta,phi,mass)
        jet.csv = csv
        jets.append(jet)
    jets.sort( key=lambda x : -x.csv )
    bjets = jets[:3]
    ljets = jets[4:]
    mass = 10000
    mass_W = 10000
    for b in range(len(bjets)):
        for i in range(len(ljets)):
            for j in range(i+1,len(ljets)):
                m = (bjets[b]+ljets[i]+ljets[j]).M()
                if abs(m-171)<abs(mass-171): 
                    mass = m
                    mass_W=(ljets[i]+ljets[j]).M()
    return mass_W
    return mass

histos.append(histoTemplate.clone( var="jets_pt[0]" , nbins=100, xmin=0, xmax=500))
#histos.append(histoTemplate.clone( var=testFunction , nbins=100, xmin=0, xmax=1000, xTitle="Wmass", treeVars={"jets_pt","jets_eta","jets_phi","jets_mass","jets_btagCSV","jets_mc*"}))

#histos.append(histoTemplate.clone( var="btag_LR_geq2b_leq1b_btagCSV" , nbins=100, xmin=0, xmax=1))
#histos.append(histoTemplate.clone( var="qg_LR_3b_flavour_5q_4q" ) )
#histos.append(histoTemplate.clone( var="qg_LR_3b_flavour_4q_3q" ) )
#histos.append(histoTemplate.clone( var="qg_LR_3b_flavour_4q_0q" ) )
#histos.append(histoTemplate.clone( var="qg_LR_3b_flavour_3q_2q" ) )
#histos.append(histoTemplate.clone( var="qg_LR_3b_flavour_3q_0q" ) )
##histos.append(histoTemplate.clone( var="qg_LR_4b_flavour_4q_4q" ) )
#histos.append(histoTemplate.clone( var="qg_LR_4b_flavour_4q_0q" ) )
#histos.append(histoTemplate.clone( var="qg_LR_4b_flavour_3q_2q" ) )
#histos.append(histoTemplate.clone( var="qg_LR_4b_flavour_3q_0q" ) )



#btag_LR_geq2b_leq1b_btagCSV
#qg_LR_4b_flavour_3q_0q




#    ("Sum$(jets_mcPt)",100, 1, 2000),
#    (test,100, 0, 1000),
#    ("nPVs",60, 0, 60),
#    ("ht",100, 0, 2000),
#    ("Sum$(jets_pt)",100, 0, 2000),
#    ("jets_pt[0]",100, 0, 1000),
#    (test,100, 0, 1000,["jets_qgl","jets_pt","jets_eta","njets","*Weight*","ht"]),
#    ("jets_pt[3]",100, 0, 200),
#    ("jets_pt[4]",100, 0, 200),
#    ("jets_pt[5]",100, 0, 200),
#    ("jets_pt[6]",100, 0, 150),
#    ("jets_pt[7]",100, 0, 100),
#    ("Max$(jets_btagCSV)",100, 0, 1),
#    ("Sum$(CSVn(jets_btagCSV,0,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_btagCSV,2,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_btagCSV,3,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_btagCMVA,3,Iteration$,Length$))",100,-1,1),
#    ("Sum$(CSVn(jets_btagCSV,4,Iteration$,Length$))",100,0,1),
#    ("jets_qgl[0]",100,0,1),
#    ("jets_qgl[1]",100,0,1),
#    ("jets_qgl[2]",100,0,1),
#    ("jets_qgl[3]",100,0,1),
#    ("jets_qgl[4]",100,0,1),
#    ("jets_qgl[5]",100,0,1),
#    ("jets_qgl[6]",100,0,1),
#    ("jets_qgl[7]",100,0,1),
#    ("jets_qgl[9]",100,0,1),
#    ("Sum$(CSVn(jets_qgl,0,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_qgl,1,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_qgl,2,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_qgl,3,Iteration$,Length$))",100,0,1),
#    ("Sum$(CSVn(jets_qgl,4,Iteration$,Length$))",100,0,1),
#    ("Sum$(jets_pt)",100, 0, 2000),
#]
'''
histos=[
    ("nPVs",60, 0, 60),
]
'''

xsec = {}
br_h_to_bb = 0.577
#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV
xsec["tth"] = 0.5085
xsec["tthbb"] = xsec["tth"] * br_h_to_bb
xsec["tthnobb"] = xsec["tth"] * (1.0 - br_h_to_bb)

xsec["tt"] = 831.76

xsec["qcd300"] = 366800.0
xsec["qcd500"] = 29370.0
xsec["qcd700"] = 6524.0
xsec["qcd1000"] = 1064.0
xsec["qcd1500"] = 121.5
xsec["qcd2000"] = 25.42


prefix = "Oct19/Oct19-__"
datasetMC = {
    "tt" : DatasetMCClass(
        xsec = xsec["tt"],
        fileName = prefix+"TT_TuneCUETP8M1_13TeV-powheg-pythia8.root",
    ),
    "tth" : DatasetMCClass(
        xsec = xsec["tth"],
        fileName = prefix+"ttHTobb_M125_13TeV_powheg_pythia8.root",
    ),
    "tthnobb" : DatasetMCClass(
        xsec = xsec["tthnobb"],
        fileName = prefix+"ttHTobb_M125_13TeV_powheg_pythia8.root",
    ),
    "qcd300" : DatasetMCClass(
        xsec = xsec["qcd300"],
        fileName = prefix+"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd500" : DatasetMCClass(
        xsec = xsec["qcd500"],
        fileName = prefix+"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd700" : DatasetMCClass(
        xsec = xsec["qcd700"],
        fileName = prefix+"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd1000" : DatasetMCClass(
        xsec = xsec["qcd1000"],
        fileName = prefix+"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd1500" : DatasetMCClass(
        xsec = xsec["qcd1500"],
        fileName = prefix+"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
    "qcd2000" : DatasetMCClass(
        xsec = xsec["qcd2000"],
        fileName = prefix+"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",
    ),
}
datasetData = {
    "JetHT" : DatasetDataClass(
        lumi = 19786,
        fileName = prefix+"JetHT.root"
    ),
}

groups =[
    GroupClass(
        color = ROOT.kGreen,
        latexName = "QCD",
        samples = ["qcd300","qcd500","qcd1000","qcd1500","qcd2000"]
#        samples = ["qcd300","qcd500","qcd700","qcd1000","qcd1500","qcd2000"]
    ),
    GroupClass(
        color = ROOT.kRed,
        latexName = "t#bar{t}",
        samples = ["tt"]
    ),
    GroupClass(
        color = ROOT.kBlue,
        latexName = "signal",
#        samples = ["tth"]
        samples = ["tth","tthnobb"]
    ),
    GroupClass(
        color = ROOT.kBlack,
        latexName = "Data",
        samples = ["JetHT"]
    ),
]


