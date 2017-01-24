#include"TChain.h"
#include"TFile.h"
#include"TH1F.h"
#include"TTreeFormula.h"
#include<iostream>
#include<string>
#include<vector>
#include"functions.C"

void splitQCDNtuplesCSV3(){
    int i; 
    bool toBeFilled;

    vector<string> fileNames_QCD;
    fileNames_QCD.push_back(string("Jan16/Dec24__QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames_QCD.push_back(string("Jan16/Dec24__QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames_QCD.push_back(string("Jan16/Dec24__QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames_QCD.push_back(string("Jan16/Dec24__QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames_QCD.push_back(string("Jan16/Dec24__QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    fileNames_QCD.push_back(string("Jan16/Dec24__QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"));
    
    
    for(const auto& fileName_QCD_: fileNames_QCD){
        auto fileName_QCD = fileName_QCD_;
        auto file_QCD            = new TFile(fileName_QCD.c_str());
        auto file_QCD_2B         = new TFile(fileName_QCD.replace(17,0,"2B_").c_str(),"recreate");
        fileName_QCD = fileName_QCD_;
        auto file_QCD_1B         = new TFile(fileName_QCD.replace(17,0,"1B_").c_str(),"recreate");
        fileName_QCD = fileName_QCD_;
        auto file_QCD_2C         = new TFile(fileName_QCD.replace(17,0,"2C_").c_str(),"recreate");
        fileName_QCD = fileName_QCD_;
        auto file_QCD_1C         = new TFile(fileName_QCD.replace(17,0,"1C_").c_str(),"recreate");
        fileName_QCD = fileName_QCD_;
        auto file_QCD_Q          = new TFile(fileName_QCD.replace(17,0,"Q_").c_str(),"recreate");
        fileName_QCD = fileName_QCD_;
        auto file_QCD_G          = new TFile(fileName_QCD.replace(17,0,"G_").c_str(),"recreate");
        fileName_QCD = fileName_QCD_;
        auto file_QCD_PU         = new TFile(fileName_QCD.replace(17,0,"PU_").c_str(),"recreate");
        
        cout << "\nI'm doing " << fileName_QCD << endl;
        
        int njets = 0;
        double jets_mcNumBHadrons[20]={};
        double jets_mcNumCHadrons[20]={};
        int jets_mcFlavour[20]={};
        double jets_btagCSV[20]={};
        
        file_QCD->cd();
        auto tree_QCD = (TTree*) file_QCD->Get("tree");
        tree_QCD->SetBranchStatus("*",1);
        tree_QCD->SetBranchAddress("njets",&njets);
        tree_QCD->SetBranchAddress("jets_mcNumBHadrons",jets_mcNumBHadrons);
        tree_QCD->SetBranchAddress("jets_mcNumCHadrons",jets_mcNumCHadrons);
        tree_QCD->SetBranchAddress("jets_mcFlavour",jets_mcFlavour);
        tree_QCD->SetBranchAddress("jets_mcFlavour",jets_mcFlavour);
        tree_QCD->SetBranchAddress("jets_btagCSV",jets_btagCSV);
        auto Count = (TH1F*) file_QCD->Get("Count");
        
        file_QCD_2B->cd();
        Count->Write();
        auto tree_QCD_2B = tree_QCD->CloneTree(0);
        
        file_QCD_1B->cd();
        Count->Write();
        auto tree_QCD_1B = tree_QCD->CloneTree(0);
        
        file_QCD_2C->cd();
        Count->Write();
        auto tree_QCD_2C = tree_QCD->CloneTree(0);
        
        file_QCD_1C->cd();
        Count->Write();
        auto tree_QCD_1C = tree_QCD->CloneTree(0);
        
        file_QCD_Q->cd();
        Count->Write();
        auto tree_QCD_Q = tree_QCD->CloneTree(0);
        
        file_QCD_G->cd();
        Count->Write();
        auto tree_QCD_G = tree_QCD->CloneTree(0);
        
        file_QCD_PU->cd();
        Count->Write();
        auto tree_QCD_PU = tree_QCD->CloneTree(0);
    
        int nentries = tree_QCD->GetEntries();
//        nentries = 10000; //############
        i=0;
        tree_QCD->GetEntry(i);
        
        for(; i<nentries; i++, tree_QCD->GetEntry(i)){
            float csv1=-30;
            float csv2=-30;
            float csv3=-30;
            int idx1 = -1;
            int idx2 = -1;
            int idx3 = -1;
            for(int i=0; i<njets;i++){
                if(jets_btagCSV[i]>csv1){
                    csv3 = csv2;
                    csv2 = csv1;
                    csv1 = jets_btagCSV[i];
                    idx3 = idx2;
                    idx2 = idx1;
                    idx1 = i;
                } else if (jets_btagCSV[i]>csv2) {
                    csv3 = csv2;
                    csv2 = jets_btagCSV[i];
                    idx3 = idx2;
                    idx2 = i;
                } else if (jets_btagCSV[i]>csv3) {
                    csv3 = jets_btagCSV[i];
                    idx3 = i;
                }
            }
            
            if( true )
            {
                    if (i%10000==0) cout << "i=" << i << endl;
                    if (idx3==-1){}
                    else if (jets_mcNumBHadrons[idx3] >= 2){
                        tree_QCD_2B->Fill();
                    }
                    else if (jets_mcNumBHadrons[idx3] == 1){
                        tree_QCD_1B->Fill();
                    }
                    else if (jets_mcNumCHadrons[idx3] >= 2){
                        tree_QCD_2C->Fill();
                    }
                    else if (jets_mcNumCHadrons[idx3] == 1){
                        tree_QCD_1C->Fill();
                    }
                    else if (abs(jets_mcFlavour[idx3]) > 0 && abs(jets_mcFlavour[idx3])<21){
                        tree_QCD_Q->Fill();
                    }
                    else if (jets_mcFlavour[idx3] == 21){
                        tree_QCD_G->Fill();
                    }
                    else if (jets_mcFlavour[idx3] == 0){
                        tree_QCD_PU->Fill();
                    } else {
                        cout << "WARNING!!! " << endl;
                    }
            }
        }
        
        file_QCD->Close();
        
        file_QCD_2B->Write();
        file_QCD_2B->Close();
        
        file_QCD_1B->Write();
        file_QCD_1B->Close();
        
        file_QCD_2C->Write();
        file_QCD_2C->Close();
        
        file_QCD_1C->Write();
        file_QCD_1C->Close();
        
        file_QCD_Q->Write();
        file_QCD_Q->Close();
        
        file_QCD_G->Write();
        file_QCD_G->Close();
        
        file_QCD_PU->Write();
        file_QCD_PU->Close();
    }
}
