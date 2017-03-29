#include"TChain.h"
#include"TFile.h"
#include"TH1F.h"
#include"TTreeFormula.h"
#include<iostream>
#include<string>
#include<vector>
#include<utility>
#include"TLorentzVector.h"

const float W_mass = 80.385;
const float Top_mass = 172.44;

float qg_sf(float qgl, int mcFlavour){
    if(qgl<0)
        return 1;
    if(mcFlavour==21) {
        return -55.7067*pow(qgl,7) + 113.218*pow(qgl,6) -21.1421*pow(qgl,5) -99.927*pow(qgl,4) + 92.8668*pow(qgl,3) -34.3663*pow(qgl,2) + 6.27*qgl + 0.612992;}
    else {
        return -0.666978*pow(qgl,3) + 0.929524*pow(qgl,2) -0.255505*qgl + 0.981581;}
}

void addQGLweights(){
    int i; 
    bool toBeFilled;

    vector<string> fileNames;
    fileNames.push_back(string("Mar27/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root"));
    fileNames.push_back(string("Mar27/TT_Plus2B.root"));
    fileNames.push_back(string("Mar27/TT_Other.root"));
    fileNames.push_back(string("Mar27/TT_PlusB.root"));
    fileNames.push_back(string("Mar27/TT_PlusBBbar.root"));
    fileNames.push_back(string("Mar27/TT_PlusCCbar.root"));
    fileNames.push_back(string("Mar27/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root"));
    fileNames.push_back(string("Mar27/JetHT.root"));
    fileNames.push_back(string("Mar27/QCDDataDriven.root"));
    fileNames.push_back(string("Mar27/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames.push_back(string("Mar27/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames.push_back(string("Mar27/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames.push_back(string("Mar27/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames.push_back(string("Mar27/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames.push_back(string("Mar27/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    
    for(const auto& fileName_: fileNames){
        auto fileName = fileName_;
        auto file               = new TFile(fileName.c_str());
        auto file_withQGLweights   = new TFile(fileName.replace(3,2,"27_withQGLweights").c_str(),"recreate");
        
        cout << "\nI'm doing " << fileName << endl;
        
        int njets = 0;
        double jets_qgl[20]={};
        int jets_mcFlavour[20]={};
        float jets_qg_sf[20]={};
        float qgWeight=0;
                
        file->cd();
        auto tree = (TTree*) file->Get("tree");
        tree->SetBranchStatus("*",1);
        tree->SetBranchAddress("njets",&njets);
        tree->SetBranchAddress("jets_qgl",jets_qgl);
        tree->SetBranchAddress("jets_mcFlavour",jets_mcFlavour);
        auto Count = (TH1F*) file->Get("Count");
        
        file_withQGLweights->cd();
        if(Count != NULL) Count->Write();
        auto tree_withQGLweights = tree->CloneTree(0);
        
        tree_withQGLweights->Branch("qgWeight",       &qgWeight,     "qgWeight/F");
        tree_withQGLweights->Branch("jets_qg_sf",     jets_qg_sf,    "jets_qg_sf[njets]/F");
                
        int nentries = tree->GetEntries();
//        nentries = 10000; //############
        i=0;
        tree->GetEntry(i);
        
        for(; i<nentries; i++, tree->GetEntry(i)){
            qgWeight = 1;
            for(int i=0; i<njets;i++){
                jets_qg_sf[i] = qg_sf(jets_qgl[i],jets_mcFlavour[i]);
                qgWeight *= jets_qg_sf[i];
                }
            tree_withQGLweights->Fill();
        }
        file->Close();
        file_withQGLweights->Write();
        file_withQGLweights->Close();
        }
}
