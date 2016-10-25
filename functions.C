#include <iostream>
#include <vector>
#include <algorithm>

std::vector<float> pts;

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
// tree->Scan("Sum$(Pt4(Jet_pt,Jet_eta,3,Iteration$,Length$)):Jet_pt[3]")



