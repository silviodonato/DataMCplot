#include"TChain.h"
#include"TFile.h"
#include"TTreeFormula.h"
#include<iostream>


void makeQCDdataDrivenSample(){
    TTreeFormula* triggerF;
    TTreeFormula* CR4bf;
    TTreeFormula* CR3bf;
    int i; 
    float xsectTT = 831.76;
    float countTT = 3.81389e+07;
    char triggerS[] = "(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v||HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v)";
    char fileTT[] = "Jan6/Jan6__TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root";
    char fileData[] = "Jan6/Jan6__JetHT.root";
    char CR4bs[] = "btag_LR_4b_2b_btagCSV>0.75 && btag_LR_4b_2b_btagCSV<0.88";
    char CR3bs[] = "btag_LR_3b_2b_btagCSV>0.6 && btag_LR_3b_2b_btagCSV<0.8 && btag_LR_4b_2b_btagCSV<0.99";
    float SR4b = 0.995;
    float SR3b = 0.995;
    float luminosity = 4600;
    
    auto fileout = new TFile("test.root","recreate");
    auto mchain = new TChain("tree");
    mchain->Add(fileTT);
    mchain->Add(fileData);
    
    
    fileout->cd();

    mchain->SetBranchStatus("*",1);
    mchain->SetBranchStatus("btag_LR_4b_2b_btagCSV",0);
    mchain->SetBranchStatus("btag_LR_3b_2b_btagCSV",0);

    auto newTree = mchain->CloneTree(0);
    mchain->SetBranchStatus("*",1);

    float qcdWeight = 0.;
    float btag_LR = 0.;
    Float_t btag_LR_4b_2b_btagCSV = 0.;
    Float_t btag_LR_3b_2b_btagCSV = 0.;
    
    newTree->Branch("qcdWeight",&qcdWeight,"qcdWeight/F");
    
    newTree->Branch("xsectTT",&xsectTT,"xsectTT/F");
    newTree->Branch("countTT",&countTT,"countTT/F");
    newTree->Branch("fileTT",&fileTT,"fileTT/C");
    newTree->Branch("fileData",&fileData,"fileData/C");
    newTree->Branch("luminosity",&luminosity,"luminosity/F");
//    newTree->SetBranchAddress("btag_LR_4b_2b_btagCSV",&btag_LR_4b_2b_btagCSV);
//    newTree->SetBranchAddress("btag_LR_3b_2b_btagCSV",&btag_LR_3b_2b_btagCSV);
    newTree->Branch("btag_LR_4b_2b_btagCSV_new",&btag_LR_4b_2b_btagCSV,"btag_LR_4b_2b_btagCSV/F");
    newTree->Branch("btag_LR_3b_2b_btagCSV_new",&btag_LR_3b_2b_btagCSV,"btag_LR_3b_2b_btagCSV/F");
    newTree->Branch("CR4b",&CR4bs,"CR4b/C");
    newTree->Branch("CR3b",&CR3bs,"CR3b/C");
    
    //Fill new tree with TTbar events (with negative weights)
    cout << "\nI'm doing TTbar\n";
    qcdWeight = -luminosity*xsectTT/countTT;
    int nentries = mchain->GetEntries();
//    nentries = 10000;
    i=0;
    mchain->GetEntry(i);
    CR4bf = new TTreeFormula("CR4bf", CR4bs, mchain->GetTree());
    CR3bf = new TTreeFormula("CR3bf", CR3bs, mchain->GetTree());
    for(; i<nentries && mchain->GetTreeNumber()==0; i++, mchain->GetEntry(i)){
                if (i%10000==0) cout << "i=" << i << endl;
                btag_LR_4b_2b_btagCSV = 0;
                btag_LR_3b_2b_btagCSV = 0;
                if (CR4bf->EvalInstance()){
                    btag_LR_4b_2b_btagCSV = 0.995;
                    newTree->Fill();
                } else if (CR3bf->EvalInstance()){
                    btag_LR_3b_2b_btagCSV = 0.995;
                    newTree->Fill();
                }
    }
    
//    i = 274074;
//    mchain->GetEntry(i);
    
    //Fill new tree with data events (with negative weights)
    cout << "\nI'm doing data\n";
    qcdWeight = 1.;
    triggerF = new TTreeFormula("triggerF", triggerS, mchain->GetTree());
    CR4bf = new TTreeFormula("CR4bf", CR4bs, mchain->GetTree());
    CR3bf = new TTreeFormula("CR3bf", CR3bs, mchain->GetTree());
    for(; i<nentries && mchain->GetTreeNumber()==1; i++, mchain->GetEntry(i)){
          if (i%10000==0) cout << "i=" << i << endl;
          if(triggerF->EvalInstance())
          {
                if (i%10000==0) cout << "i=" << i << endl;
                btag_LR_4b_2b_btagCSV = 0;
                btag_LR_3b_2b_btagCSV = 0;
                if (CR4bf->EvalInstance()){
                    btag_LR_4b_2b_btagCSV = SR4b;
                    newTree->Fill();
                } else if (CR3bf->EvalInstance()){
                    btag_LR_3b_2b_btagCSV = SR3b;
                    newTree->Fill();
                }
          }
    }
    newTree->Write();
}