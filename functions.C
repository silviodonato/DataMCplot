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

float trigger450(float ht, float pt6){
//    float value = 0.00519011+1.27471*0.25*(1.+erf((pt6-37.7919)/9.36544))*(1+erf((ht-429.892)/84.6407))/2;
    float value = 0.00369199+1.30284*0.25*(1.+erf((pt6-38.2357)/10.9048))*(1+erf((ht-426.231)/76.4188))/2;
    return between0and1(value);

}

float triggerCSV450(float ht, float pt6, float csv1){
    float value = trigger450(ht, pt6) / 0.642545;
    value = value * (-0.186534+2.87872*csv1+-7.43255*pow(csv1,2)+9.70895*pow(csv1,3)-3.97967*pow(csv1,4));
    return between0and1(value);
}

float trigger400(float ht, float pt6){
//    float value = -0.0152737+0.779279*0.25*(1.+erf((pt6-13.4755)/50))*(1+erf((ht-349.617)/64.0324))/2;
    float value = 0.0612614+0.432906*0.25*(1.+erf((pt6-26.5964)/22.6479))*(1+erf((ht-362.727)/57.5796))/2;
    return between0and1(value);
}

float triggerCSV400(float ht, float pt6, float csv1, float csv2){
    float value = trigger400(ht, pt6) / 0.374366;
    value = value * 0.010907+(0.564039*csv1+1.2244*pow(csv1,2))*(-0.0702136*csv2+0.615238*pow(csv2,2));
    return between0and1(value);
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



