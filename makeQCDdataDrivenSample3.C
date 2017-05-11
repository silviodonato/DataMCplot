#include"TChain.h"
#include"TFile.h"
#include"TH1F.h"
#include"TTreeFormula.h"
#include"string.h"
#include<iostream>


void makeQCDdataDrivenSample3(){
//////  KEEP ME UPDATED !!!! ////////
    float luminosity = 36546;
//    char fileMC[] = "Apr27/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root";
    char fileData[] = "Apr27/JetHT.root";

    vector<std::pair<string,float> > MCs;
    MCs.push_back(std::pair<string,float>(string(
        "Apr27_WithHiggsMass/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
        ),
        25.42
        ));
    MCs.push_back(std::pair<string,float>(string(
        "Apr27_WithHiggsMass/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
        ),
        121.5
        ));
    MCs.push_back(std::pair<string,float>(string(
        "Apr27_WithHiggsMass/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
        ),
        1064.0
        ));
    MCs.push_back(std::pair<string,float>(string(
        "Apr27_WithHiggsMass/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root"
        ),
        831.76
        ));

///////////////////////////
    
    float xsectMC = 831.76;
    
    TTreeFormula* triggerF;
    TTreeFormula* cutF;
    TTreeFormula* CR4bf;
    TTreeFormula* CR3bf;
    int i; 
    bool toBeFilled;
    string fileMC;
    
    char triggerS[] = "(HLT_BIT_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v||HLT_BIT_HLT_PFHT450_SixJet40_BTagCSV_p056_v)";
//    char cutS[] = "Alt$(jets_pt[5],0)>50 && ht40>600 && Sum$(jets_btagCSV>0.8)>=2";
    
    char CR4bs[] = "nBCSVM==3 && Sum$(jets_btagCSV>0.5426)==4";
    char CR3bs[] = "nBCSVM==2 && Sum$(jets_btagCSV>0.5426)==3";
    char fileName[200];
    
    int SR4b = 4;
    int SR3b = 3;
    
    float countMC;
    
    auto fileout = new TFile("test.root","recreate");
    auto mchain = new TChain("tree");
    for (auto& MC : MCs) {
        mchain->Add(TString(MC.first));
    }
    mchain->Add(fileData);
    
    mchain->SetBranchStatus("*",1);
    mchain->SetBranchStatus("nBCSVM",0);

    fileout->cd();

    auto newTree = mchain->CloneTree(0);
    mchain->SetBranchStatus("*",1);

    float qcdWeight = 0.;
    float btag_LR = 0.;
    Int_t nBCSVM = 0.;
    
    newTree->Branch("qcdWeight",&qcdWeight,"qcdWeight/F");
    
    newTree->Branch("xsectMC",&xsectMC,"xsectMC/F");
    newTree->Branch("countMC",&countMC,"countMC/F");
    newTree->Branch("fileName",&fileName,"fileName/C");
    newTree->Branch("luminosity",&luminosity,"luminosity/F");
    newTree->Branch("nBCSVM_new",&nBCSVM,"nBCSVM/I");
    newTree->Branch("CR4b",&CR4bs,"CR4b/C");
    newTree->Branch("CR3b",&CR3bs,"CR3b/C");
    
    //Fill new tree with TTbar events (with negative weights)
    int nentries = mchain->GetEntries();
//    nentries = 10000; ##############################
    i=0;
    cout << MCs.size() ;
    for(unsigned int mc; mc<MCs.size(); mc++){
        fileMC = MCs.at(mc).first;
        strcpy(fileName, fileMC.c_str());
        
        auto fileMC_ = new TFile(TString(fileMC));
        float countMC = ((TH1F*) fileMC_->Get("Count"))->GetBinContent(1);
        
        xsectMC = MCs.at(mc).second;
        qcdWeight = -luminosity*xsectMC/countMC;
        mchain->GetEntry(i);
        triggerF = new TTreeFormula("triggerF", triggerS, mchain->GetTree());
    //    cutF = new TTreeFormula("cutF", cutS, mchain->GetTree());
        CR4bf = new TTreeFormula("CR4bf", CR4bs, mchain->GetTree());
        CR3bf = new TTreeFormula("CR3bf", CR3bs, mchain->GetTree());
        cout << "\nI'm doing "<< fileMC << endl;
        cout << "\ncountMC = "<< countMC << endl;
        cout << "\nxsectMC = "<< xsectMC << endl;
        for(int count = 0; i<nentries && mchain->GetTreeNumber()==mc; i++, mchain->GetEntry(i), count ++){
    //        if(cutF->EvalInstance())
            if (i%10000==0) cout << "i=" << i << endl;
            if(triggerF->EvalInstance())
            {
                    nBCSVM = -1;
                    if (CR4bf->EvalInstance()){
                        nBCSVM = SR4b;
                        toBeFilled = true;
                    }
                    else if (CR3bf->EvalInstance()){
                        nBCSVM = SR3b;
                        toBeFilled = true;
                    }
                    if (toBeFilled) newTree->Fill();
            }
        }
    fileMC_->Close();
    }
    
//    i = 274074;
//    mchain->GetEntry(i);
    
    //Fill new tree with data events (with negative weights)
    cout << "\nI'm doing data\n";
    strcpy(fileName, fileData);
    qcdWeight = 1.;
    triggerF = new TTreeFormula("triggerF", triggerS, mchain->GetTree());
//    cutF = new TTreeFormula("cutF", cutS, mchain->GetTree());
    CR4bf = new TTreeFormula("CR4bf", CR4bs, mchain->GetTree());
    CR3bf = new TTreeFormula("CR3bf", CR3bs, mchain->GetTree());
    for(int count = 0; i<nentries; i++, mchain->GetEntry(i), count ++){
          if (i%10000==0) cout << "i=" << i << endl;
//          if(triggerF->EvalInstance() && cutF->EvalInstance())
//          if(triggerF->EvalInstance())
          if(true)
          {
                nBCSVM = -1;
//                if (CR4bf->EvalInstance()){
//                    nBCSVM = SR4b;
//                    toBeFilled = true;
//                }
//                else if (CR3bf->EvalInstance()){
//                    nBCSVM = SR3b;
//                    toBeFilled = true;
//                }
                if (toBeFilled) newTree->Fill();
          }
    }
    fileout->cd();
    newTree->Write();
    fileout->Close();
}
