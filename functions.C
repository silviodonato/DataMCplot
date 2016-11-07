#include <iostream>
#include <vector>
#include <algorithm>
#include "TLorentzVector.h"

std::vector<float> pts;

float prod;

TLorentzVector part1;
TLorentzVector part2;

float CSVn(float csv, int n, int iteration, int length){
    using namespace std;
    float value = 0;
    if(iteration==0){
        pts.clear();
    }
    pts.push_back(csv);
    if (iteration==length-1){
        std::sort(pts.begin(),pts.end());
        std::reverse(pts.begin(),pts.end());
        if (pts.size()>n){
            value= pts[n];
            pts.clear();
        }
    }
    return value;
}

// tree->Scan("Sum$(CSVn(jets_btagCSV,1,Iteration$,Length$))")
// tree->Scan("Sum$(Pt4(Jet_pt,Jet_eta,3,Iteration$,Length$)):Jet_pt[3]")

float between0and1(float x){
    if (x>1)
        x = 1;
    else if (x<0)
        x = 0;
    return x;
}

//######################s80 only

//float trigger400(float ht, float pt6){
//    float value = 0.0726933+0.83076*0.25*(1.+erf((pt6-6.12049)/40.0755))*(1+erf((ht-427.892)/42.9944))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.0195169+1.51545*0.25*(1.+erf((pt6-42.0503)/7.87602))*(1+erf((ht-473.08)/83.2179))/2;
//    return between0and1(value);
//}

//######################s140 only
//float trigger400(float ht, float pt6){
//    float value = 0.16841+0.648461*0.25*(1.+erf((pt6-29.1189)/19.4484))*(1+erf((ht-429.667)/26.8442))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.192428+1.9955*0.25*(1.+erf((pt6-40.8081)/8.44953))*(1+erf((ht-424.985)/147.851))/2;
//    return between0and1(value);
//}

//######################s450 only

//float trigger400(float ht, float pt6){
//    float value = -0.379812+1.16887*0.25*(1.+erf((pt6-16.784)/16.5186))*(1+erf((ht-373.466)/25.0661))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.430269+2*0.25*(1.+erf((pt6-37.1773)/11.3937))*(1+erf((ht-211.371)/74.1368))/2;
//    return between0and1(value);
//}

//######################d60 only

//float trigger400(float ht, float pt6){
//    float value = 0.037519+0.613332*0.25*(1.+erf((pt6-39.6717)/5.25521))*(1+erf((ht-345.569)/150))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.0547637+1.42316*0.25*(1.+erf((pt6-41.2995)/6.83003))*(1+erf((ht-438.035)/150))/2;
//    return between0and1(value);
//}

//######################d80 only

//float trigger400(float ht, float pt6){
//    float value = 0.0515132+0.906264*0.25*(1.+erf((pt6-29.8166)/11.6635))*(1+erf((ht-420.467)/25))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.01681+1.58632*0.25*(1.+erf((pt6-42.4488)/7.08872))*(1+erf((ht-485.994)/54.527))/2;
//    return between0and1(value);
//}

//######################d140 only

//float trigger400(float ht, float pt6){
//    float value = 0.354395+0.236505*0.25*(1.+erf((pt6-40.6406)/18.772))*(1+erf((ht-474.501)/150))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.0965839+1.86651*0.25*(1.+erf((pt6-41.4983)/8.46008))*(1+erf((ht-452.245)/150))/2;
//    return between0and1(value);
//}

//######################d320 only

//float trigger400(float ht, float pt6){
//    float value = -0.30605+1.24401*0.25*(1.+erf((pt6-14.2244)/20.5593))*(1+erf((ht-200.405)/25.0017))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.294139+2*0.25*(1.+erf((pt6-39.2306)/10.2617))*(1+erf((ht-200.005)/73.9849))/2;
//    return between0and1(value);
//}

//######################all single only

//float trigger400(float ht, float pt6){
//    float value = 0.087871+0.293572*0.25*(1.+erf((pt6-35.1372)/3.75796))*(1+erf((ht-403.488)/25))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.0174406+1.23285*0.25*(1.+erf((pt6-41.5783)/8.11809))*(1+erf((ht-451.985)/50.3688))/2;
//    return between0and1(value);
//}

//######################all single only - test

//float trigger400(float ht, float pt6){
//    float value = 0.112524+0.116443*0.25*(1.+erf((pt6-13.1114)/5.35263))*(1+erf((ht-410.159)/1.7786));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.132483+0.735719*0.25*(1.+erf((pt6-40.3558)/9.13524))*(1+erf((ht-429.459)/75.5132));
//    return between0and1(value);
//}

//######################all single only - test2
//float trigger400(float ht, float pt6){
//    float value = 0.112485+0.121765*0.25*(1.+erf((pt6-6.07848)/1.06471))*(1+erf((ht-410.203)/1.09225));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.0617072+0.661049*0.25*(1.+erf((pt6-41.0791)/8.47252))*(1+erf((ht-443.681)/60.6348));
//    return between0and1(value);
//}


//######################all single only - test3

//float trigger400(float ht, float pt6){
//    float value = 0.112536+0.116432*0.25*(1.+erf((pt6-2.20704)/1.48607))*(1+erf((ht-411.739)/1.09948));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.127541+0.730657*0.25*(1.+erf((pt6-40.4075)/9.09909))*(1+erf((ht-430.436)/74.4073));
//    return between0and1(value);
//}

//######################all single only - test4

//float trigger400(float ht, float pt6){
//    float value = 0.113137+0.225216*0.25*(1.+erf((pt6-27.2679)/13.6761))*(1+erf((ht-401.373)/15.9876));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.0285152+0.696121*0.25*(1.+erf((pt6-42.6947)/7.83462))*(1+erf((ht-456.103)/46.785));
//    return between0and1(value);
//}

//######################all single only - test4b
//float trigger400(float ht, float pt6){
//    float value = 0.114238+0.233151*0.25*(1.+erf((pt6-0.751248)/38.2597))*(1+erf((ht-402.186)/16.1529));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.0122951+0.707302*0.25*(1.+erf((pt6-42.4282)/8.22221))*(1+erf((ht-452.616)/50.5748));
//    return between0and1(value);
//}

//######################all single only - test4c
//float trigger400(float ht, float pt6){
//    float value = 0.228493+5.37551e-11*0.25*(1.+erf((pt6-8.85481)/49.2917))*(1+erf((ht-203.261)/35.517));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.00838442+0.593602*0.25*(1.+erf((pt6-41.9341)/7.99215))*(1+erf((ht-445.307)/37.7146));
//    return between0and1(value);
//}

//######################all single only - up to 320

//float trigger400(float ht, float pt6){
//    float value = 0.115357+0.206079*0.25*(1.+erf((pt6-31.307)/8.11978))*(1+erf((ht-400.769)/15.3341));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.00575456+0.718067*0.25*(1.+erf((pt6-42.1232)/8.58142))*(1+erf((ht-449.407)/54.6631));
//    return between0and1(value);
//}

//######################all single only - up to 320 + L1 VBF
 
 float trigger400(float ht, float pt6){
    float value = 0.0249284+0.316144*0.25*(1.+erf((pt6-25.0156)/14.8097))*(1+erf((ht-423.709)/42.8797));
    return between0and1(value / 0.341072);
}

float trigger450(float ht, float pt6){
    float value = 0.0183759+0.698898*0.25*(1.+erf((pt6-42.4901)/8.17063))*(1+erf((ht-459.777)/44.0002));
    return between0and1(value / 0.717274);
}


//######################all single only - test5

//float trigger400(float ht, float pt6){
//    float value = 0.228493+5.37551e-11*0.25*(1.+erf((pt6-8.85481)/49.2917))*(1+erf((ht-203.261)/35.517));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.00838442+0.593602*0.25*(1.+erf((pt6-41.9341)/7.99215))*(1+erf((ht-445.307)/37.7146));
//    return between0and1(value);
//}

//###################### L1 VBF

//float trigger400(float ht, float pt6){
//    float value = 0.0247552+0.515348*0.25*(1.+erf((pt6-56.8937)/50))*(1+erf((ht-416.511)/32.8908));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.018798+0.596831*0.25*(1.+erf((pt6-42.3461)/6.07722))*(1+erf((ht-481.238)/51.0513));
//    return between0and1(value);
//}

//###################### L1 VBF + single jet

//float trigger400(float ht, float pt6){
//    float value = 0.0386743+0.190434*0.25*(1.+erf((pt6-29.9311)/2.81126))*(1+erf((ht-411.084)/19.2638));
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.016587+0.585518*0.25*(1.+erf((pt6-42.0379)/7.90142))*(1+erf((ht-467.237)/41.2733));
//    return between0and1(value);
//}

//######################all single only -test

//float trigger400(float ht, float pt6){
//    float value = 0.00552438+2.07612e-14*0.25*(1.+erf((pt6-60)/47.0284))*(1+erf((ht-207.623)/9.3937))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = -0.127558+1.46135*0.25*(1.+erf((pt6-40.4073)/9.09919))*(1+erf((ht-430.433)/74.4097))/2;
//    return between0and1(value);
//}


//######################all double only

//float trigger400(float ht, float pt6){
//    float value = 0.042995+0.613103*0.25*(1.+erf((pt6-18.3443)/2.56516))*(1+erf((ht-412.842)/25))/2;
//    return between0and1(value);
//}

//float trigger450(float ht, float pt6){
//    float value = 0.0124833+1.41466*0.25*(1.+erf((pt6-42.3613)/8.16697))*(1+erf((ht-473.002)/49.1664))/2;
//    return between0and1(value);
//}

//######################

//float trigger450(float ht, float pt6){
//    float value = 0.00214235+1.23743*0.25*(1.+erf((pt6-38.1227)/10.9508))*(1+erf((ht-427.268)/79.2495))/2;
//    return between0and1(value);
//}

/*
float trigger400(float ht, float pt6){
float value = 0.0612614+0.432906*0.25*(1.+erf((pt6-26.5964)/22.6479))*(1+erf((ht-362.727)/57.5796))/2;
    return between0and1(value);
}

float trigger450(float ht, float pt6){
float value = 0.00369199+1.30284*0.25*(1.+erf((pt6-38.2357)/10.9048))*(1+erf((ht-426.231)/76.4188))/2;
    return between0and1(value);
}
*/


float triggerCSV400(float ht, float pt6, float csv2){
    float value = trigger400(ht, pt6);
    value = value * (0.0685113-1.24983*csv2+8.97234*pow(csv2,2)-23.8342*pow(csv2,3)+29.3372*pow(csv2,4)-12.3525*pow(csv2,5));
    return between0and1(value);
}

float triggerCSV450(float ht_40, float pt6, float csv1){
    float value = trigger450(ht_40, pt6);
    value = value * (0.00724648+0.532534*csv1+2.48397*pow(csv1,2)-9.78714*pow(csv1,3)+13.8441*pow(csv1,4)-6.09396*pow(csv1,5));
    return between0and1(value);
}

float triggerCSV450_and_CSV400(float ht_40, float pt6, float csv2){
    float value = trigger450(ht_40, pt6);
    value = value * (0.0685113-1.24983*csv2+8.97234*pow(csv2,2)-23.8342*pow(csv2,3)+29.3372*pow(csv2,4)-12.3525*pow(csv2,5));
    return between0and1(value);
}

float triggerCSV450_or_CSV400(float ht_30, float ht_40, float pt6, float csv1, float csv2){
    float value = triggerCSV400(ht_30, pt6, csv2) + triggerCSV450(ht_40, pt6, csv1) - triggerCSV450_and_CSV400(ht_40, pt6, csv2);
    return between0and1(value);
}

float puWeightICHEP(float puWeight, float puWeightDown){
    float value = puWeight*(1+2.8*(puWeightDown-puWeight)/puWeight);
    if(value<0) value = 0;
    return value*0.921941627;
}

float puWeightICHEP400(float puWeight, float puWeightDown){
    float value = puWeight*(1+14.7*(puWeightDown-puWeight)/puWeight);
    if(value<0) value = 0;
    return value*0.921941627/2.25837;
}

float puWeightICHEP450(float puWeight, float puWeightDown){
    float value = puWeight*(1+12.2*(puWeightDown-puWeight)/puWeight);
    if(value<0) value = 0;
    return value*0.921941627/1.97288;
}

float qg_sf(float qgl, int mcFlavour){
    if(qgl<0) 
        return 1;
    if(mcFlavour==21) {
        return -55.7067*pow(qgl,7) + 113.218*pow(qgl,6) -21.1421*pow(qgl,5) -99.927*pow(qgl,4) + 92.8668*pow(qgl,3) -34.3663*pow(qgl,2) + 6.27*qgl + 0.612992;}
    else {
        return -0.666978*pow(qgl,3) + 0.929524*pow(qgl,2) -0.255505*qgl + 0.981581;}
}

float product(float x, int iteration, int length){
    if(iteration==0){
        prod = 1;
    }
    prod = prod * x ;
    if (iteration==length-1){
        return prod;
    } else{
        return 0;
    }
}

float transverseMass(float pt1, float phi1, float pt2, float phi2){
    part1.SetPtEtaPhiM(pt1,0,phi1,0);
    part2.SetPtEtaPhiM(pt2,0,phi2,0);
    return (part1+part2).M();
}

// Sum$(product(jets_pt,Iteration$,Length$))

//gluoni: -55.7067 113.218 -21.1421 -99.927 92.8668 -34.3663 6.27 0.612992
//quarks: -0.666978 0.929524 -0.255505 0.981581

//ht:Alt$(jets_pt[5],0)

// 450
//'0.00519011+1.27471*0.25*(1.+erf((Alt$(jets_pt[5],0)-37.7919)/9.36544))*(1+erf((ht-429.892)/84.6407))/2'


// 400
//..'-0.0152737+0.779279*0.25*(1.+erf((Alt$(jets_pt[5],0)-13.4755)/50))*(1+erf((ht-349.617)/64.0324))/2'

//'-0.186534+2.87872*x+-7.43255*pow(x,2)+9.70895*pow(x,3)+-3.97967*pow(x,4)'

//'0.010907+(0.564039*x+1.2244*pow(x,2))*(-0.0702136*y+0.615238*pow(y,2))'



