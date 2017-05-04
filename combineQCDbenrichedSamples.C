#include"TChain.h"
#include"TFile.h"
#include"TH1F.h"
#include"TList.h"
#include"TString.h"
#include<iostream>


void combineQCDbenrichedSamples(){
    TString HTs[] = {"HT300to500","HT500to700","HT700to1000","HT1000to1500","HT1500to2000","HT2000toInf"};
    
    float stat_increase;
    TList* list;
    
    for (auto &ht: HTs){
        TString fileInclusive  = TString("Apr27/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root");
        TString fileBGenFilter = TString("Apr27/QCD_HT300to500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root");
        TString fileBEnriched  = TString("Apr27/QCD_bEnriched_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root");

        TString outNoB  = TString("Apr27/QCD_HT300to500_NoB.root");
        TString outBGenFilter = TString("Apr27/QCD_HT300to500_BGenFilter_merged.root");
        TString outBEnriched  = TString("Apr27/QCD_HT300to500_bEnriched_merged.root");

        fileInclusive.ReplaceAll(TString("HT300to500"),ht);
        fileBGenFilter.ReplaceAll(TString("HT300to500"),ht);
        fileBEnriched.ReplaceAll(TString("HT300to500"),ht);
        outNoB.ReplaceAll(TString("HT300to500"),ht);
        outBGenFilter.ReplaceAll(TString("HT300to500"),ht);
        outBEnriched.ReplaceAll(TString("HT300to500"),ht);

        cout << fileInclusive << endl;

        char NoBS[] = "lheNb==0 && nGenStatus2bHad==00";
        char BGenFilterS[] = "lheNb==0 && nGenStatus2bHad>0";
        char BEnrichedS[]  = "lheNb>0";
        
        auto fileInclusive_ = new TFile(fileInclusive);
        auto fileBGenFilter_ = new TFile(fileBGenFilter);
        auto fileBEnriched_ = new TFile(fileBEnriched);

        auto treeInclusive = (TTree*) fileInclusive_->Get("tree");
        auto treeBGenFilter = (TTree*) fileBGenFilter_->Get("tree");
        auto treeBEnriched = (TTree*) fileBEnriched_->Get("tree");
        
        auto countInclusive = (TH1F*) fileInclusive_->Get("CountWeighted");

        //NoB file
        auto fileoutNoB = new TFile(outNoB,"recreate");
        fileoutNoB->cd();
        TTree* outtreeNoB = treeInclusive->CopyTree(NoBS);
        countInclusive->Write();
        outtreeNoB->Write();
        float count = countInclusive->GetBinContent(1);
        fileoutNoB->Close();
        
        //BGenFilter file
        auto fileoutBGenFilter = new TFile(outBGenFilter,"recreate");
        fileoutBGenFilter->cd();
        TTree* outtreeBGenFilter = treeInclusive->CopyTree(BGenFilterS);
        stat_increase = 1.*treeBGenFilter->GetEntries()/outtreeBGenFilter->GetEntries();
        list = new TList();
        list->Add(treeBGenFilter);
        outtreeBGenFilter->Merge(list);
        outtreeBGenFilter->Write();
        countInclusive->SetBinContent(1,count*(1.+stat_increase));
        countInclusive->Write();
        fileoutBGenFilter->Close();
        
        //BEnriched file
        auto fileoutBEnriched = new TFile(outBEnriched,"recreate");
        fileoutBEnriched->cd();
        TTree* outtreeBEnriched = treeInclusive->CopyTree(BEnrichedS);
        stat_increase = 1.*treeBEnriched->GetEntries()/outtreeBEnriched->GetEntries();
        list = new TList();
        list->Add(treeBEnriched);
        outtreeBEnriched->Merge(list);
        outtreeBEnriched->Write();
        countInclusive->SetBinContent(1,count*(1.+stat_increase));
        countInclusive->Write();
        fileoutBEnriched->Close();
        
        fileBEnriched_->Close();
        fileInclusive_->Close();
        fileBGenFilter_->Close();
        }
    
}
