#include"TChain.h"
#include"TFile.h"
#include"TH1F.h"
#include"TTreeFormula.h"
#include<iostream>

void splitTTbarNtuples(){
    int i; 
    bool toBeFilled;
    
    char ttbarPlusBS[] = "ttCls == 51";
    char ttbarPlus2BS[] = "ttCls == 52";
    char ttbarPlusBBbarS[] = "ttCls >= 53";
    char ttbarPlusCCbarS[] = "ttCls >= 41 && ttCls<=45";
    char ttbarOtherS[] = "1";
    
    char fileName_TT[] = "Jan16/Jan6__TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root";
    
    char fileName_TTPlusB[] = "Jan16/Jan6__TT_PlusB.root";
    char fileName_TTPlusBBbar[] = "Jan16/Jan6__TT_PlusBBbar.root";
    char fileName_TTPlus2B[] = "Jan16/Jan6__TT_Plus2B.root";
    char fileName_TTPlusCCbar[] = "Jan16/Jan6__TT_PlusCCbar.root";
    char fileName_TTOther[] = "Jan16/Jan6__TT_Other.root";
    
    auto file_TT            = new TFile(fileName_TT);
    auto file_TTPlusB       = new TFile(fileName_TTPlusB,"recreate");
    auto file_TTPlusBBbar   = new TFile(fileName_TTPlusBBbar,"recreate");
    auto file_TTPlus2B      = new TFile(fileName_TTPlus2B,"recreate");
    auto file_TTPlusCCbar   = new TFile(fileName_TTPlusCCbar,"recreate");
    auto file_TTOther       = new TFile(fileName_TTOther,"recreate");
    
    file_TT->cd();
    
    auto treeTT = (TTree*) file_TT->Get("tree");
    auto Count = (TH1F*) file_TT->Get("Count");
    treeTT->SetBranchStatus("*",1);
    
    file_TTPlusB->cd();
    Count->Write();
    auto tree_TTPlusB = treeTT->CloneTree(0);

    file_TTPlusBBbar->cd();
    Count->Write();
    auto tree_TTPlusBBbar = treeTT->CloneTree(0);
    
    file_TTPlus2B->cd();
    Count->Write();
    auto tree_TTPlus2B = treeTT->CloneTree(0);
    
    file_TTPlusCCbar->cd();
    Count->Write();
    auto tree_TTPlusCCbar = treeTT->CloneTree(0);
    
    file_TTOther->cd();
    Count->Write();
    auto tree_TTOther = treeTT->CloneTree(0);
    
    cout << "\nI'm doing TTbar\n";
    int nentries = treeTT->GetEntries();
//    nentries = 10000;
    i=0;
    treeTT->GetEntry(i);
    
    auto ttbarPlusBF = new TTreeFormula("ttbarPlusBF", ttbarPlusBS, treeTT);
    auto ttbarPlusBBbarF = new TTreeFormula("ttbarPlusBBbarF", ttbarPlusBBbarS, treeTT);
    auto ttbarPlus2BF = new TTreeFormula("ttbarPlus2BF", ttbarPlus2BS, treeTT);
    auto ttbarPlusCCbarF = new TTreeFormula("ttbarPlusCCbarF", ttbarPlusCCbarS, treeTT);
    auto ttbarOtherF = new TTreeFormula("ttbarPlusOtherF", ttbarOtherS, treeTT);
    
    for(; i<nentries; i++, treeTT->GetEntry(i)){
        if( true )
        {
                if (i%10000==0) cout << "i=" << i << endl;
                if (ttbarPlusBF->EvalInstance()){
                    tree_TTPlusB->Fill();
                }
                else if (ttbarPlusBBbarF->EvalInstance()){
                    tree_TTPlusBBbar->Fill();
                }
                else if (ttbarPlus2BF->EvalInstance()){
                    tree_TTPlus2B->Fill();
                }
                else if (ttbarPlusCCbarF->EvalInstance()){
                    tree_TTPlusCCbar->Fill();
                }
                else if (ttbarOtherF->EvalInstance()){
                    tree_TTOther->Fill();
                }
        }
    }
    
    file_TT->Close();
    
    file_TTPlusB->Write();
    file_TTPlusB->Close();
    
    file_TTPlusBBbar->Write();
    file_TTPlusBBbar->Close();
    
    file_TTPlus2B->Write();
    file_TTPlus2B->Close();
    
    file_TTPlusCCbar->Write();
    file_TTPlusCCbar->Close();
    
    file_TTOther->Write();
    file_TTOther->Close();
}
