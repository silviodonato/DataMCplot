from glob import glob
import ROOT
import array
import os,sys

printLineNull = True
printLineSignif = True
printLineSignifN = True

def findBestCut(background, signal):
    xaxis = background.GetXaxis()
    xaxis_check = signal.GetXaxis()
    assert ( xaxis.GetNbins()==xaxis_check.GetNbins() and xaxis.GetXmax()==xaxis_check.GetXmax() and xaxis.GetXmin()==xaxis_check.GetXmin() )
    nbins = xaxis.GetNbins()
    
    bkg_tot = background.Integral(0,nbins+1)
    sig_tot = signal.Integral(0,nbins+1)
    ## nbins+3: first bin zero + nbins + overflow + underflow
    bkg_int = [0]*(nbins+3)
    sig_int = [0]*(nbins+3)
    sig_eff = [0]*(nbins+3)
    bkg_rej = [0]*(nbins+3)
    for i in range(1,nbins+3):
        sig_int[i] = (sig_int[i-1]+signal.GetBinContent(i-1))
        bkg_int[i] = (bkg_int[i-1]+background.GetBinContent(i-1))
    
#    ## possible check
#    print bkg_int[nbins+2],"=",background.Integral(0,nbins+1)
#    print sig_int[nbins+2],"=",signal.Integral(0,nbins+1)
    
    bkg_tot = bkg_int[nbins+2]
    sig_tot = sig_int[nbins+2]
    
    if bkg_tot==0 : bkg_tot=1E-6
    if sig_tot==0 : sig_tot=1E-6

    bestS2_B = -3
    bestCut = 0
    bestBinCut = 0
    inverted = True
    for i in range(0,nbins+3):
        sig_eff[i] = sig_int[i]/sig_tot
        bkg_rej[i] = 1 - bkg_int[i]/bkg_tot
        if inverted:
            sig_eff[i] = 1 - sig_eff[i]
            bkg_rej[i] = 1 - bkg_rej[i]
        ## find the best cuts (highest eff/sqrt(1-rej) or eff**2/(1-rej))
        S2_B = sig_eff[i]*sig_eff[i]/(1.0001-bkg_rej[i])
        if S2_B>bestS2_B:
            bestBinCut = i
            bestS2_B = S2_B
    bestCut = xaxis.GetBinLowEdge(bestBinCut)
    
    return bestCut,bestBinCut

def doCutAndCount(fileName):
    print "I'm doing ",fileName
    file_ = ROOT.TFile(fileName)
    c1 = file_.Get("c2")
    list_ = c1.GetListOfPrimitives()[1].GetListOfPrimitives()
    stack = list_[1]
    background = stack.GetStack().Last().Clone("background")
    signal = list_[2]
    
    bestCut,binCut = findBestCut(background,signal)
    nbins = background.GetXaxis().GetNbins()
    
    hists = stack.GetHists()
    sigYield = 0
    bkgYield = 0
    print
    print "Cut: ", bestCut
    print
    for hist in hists:
        name = hist.GetName().split("_")[1]
        yield_ = hist.Integral(binCut,nbins+1)
        print name, round(yield_,1)
        if "signal" in name:
            sigYield += yield_
        else:
            bkgYield += yield_
    print
    print "S = ", round(sigYield,1)
    print "B = ", round(bkgYield,1)
    print "S/B (%) = ", round(sigYield/bkgYield*100,1)
    print "S/sqrt(B) = ", round(sigYield/(bkgYield)**0.5,2)
    scale = 36.7/10.6
    print "S/sqrt(B) [36.7fb-1] = ", round(sigYield*scale/(bkgYield*scale)**0.5,2)
    print
if __name__ == "__main__":
    ROOT.gROOT.SetBatch()
    inputFiles = sys.argv[1:]
    print "Input files: ", inputFiles
    
    doCutAndCount("plots_ddQCDcatQGL_SR_7j3b/root/MEMratio.root")
    doCutAndCount("plots_ddQCDcatQGL_SR_7j4b/root/MEMratio.root")
    doCutAndCount("plots_ddQCDcatQGL_SR_8j3b/root/MEMratio.root")
    doCutAndCount("plots_ddQCDcatQGL_SR_8j4b/root/MEMratio.root")
    doCutAndCount("plots_ddQCDcatQGL_SR_9j3b/root/MEMratio.root")
    doCutAndCount("plots_ddQCDcatQGL_SR_9j4b/root/MEMratio.root")
    
'''
    for inputFile in inputFiles:
        files = glob(inputFile) ## solve possible wildcard characters
        for file_ in files:
            doCutAndCount(file_)
            print "\n"
'''
    

