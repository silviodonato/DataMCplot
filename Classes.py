import ROOT
import copy

class DatasetClass(object):
    def __init__(self, fileName):
        self.fileName = fileName
    def loadTree(self):
        self.tfile = ROOT.TFile(self.fileName)
        self.tree = self.tfile.Get("tree")
        print "Getting tree from ",self.fileName #," id=",id(self.tree)
        assert(type(self.tree)==ROOT.TTree)
    def closeFile(self):
        self.tfile.Close()

class DatasetMCClass(DatasetClass):
    def __init__(self, xsec, fileName):
        DatasetClass.__init__(self, fileName)
        self.xsec = xsec
        self.count = self.getCount()
    def getCount(self):
        return self.tfile.Get("CountWeighted").GetBinContent(1)
    def setSingleEventWeight(self,lumi):
        self.singleEventWeight = lumi * self.xsec / self.count
        

class DatasetDataClass(DatasetClass):
    def __init__(self, lumi, fileName):
        DatasetClass.__init__(self, fileName)
        self.lumi = lumi #pb

class GroupClass():
    def __init__(self, color, latexName, samples):
        self.color = color
        self.latexName = latexName
        self.samples = samples
        for sample in samples:
            if not hasattr(sample,"tree")
                sample.loadTree()
            else:
                print "Check the group definition: you are using a sample two times!"

class HistogramClass():
    def __init__(self, var, nbins, xmin, xmax, folder, weightMC, cutsMC, cutsData, treeVars=set(), xTitle="", yTitle="", plotName="", opts=""):
        self.var = var
        self.nbins = nbins
        self.xmin = xmin
        self.xmax = xmax
        self.folder = folder
        self.weightMC = weightMC
        self.cutsMC = cutsMC
        self.cutsData = cutsData
        self.plotName = plotName
        self.xTitle = xTitle
        self.yTitle = yTitle
        self.opts = opts
        self.treeVars = treeVars
        self.init()
        
    def init(self):
        if self.xTitle == "": self.xTitle = self.var
        if self.plotName=="": self.plotName = filter(str.isalnum, self.xTitle)
        bin_size = 1.*(self.xmax-self.xmin)/self.nbins
        if self.yTitle == "": self.yTitle = "Events/"+str(bin_size)
        if self.opts == "": self.opts = "HIST goff"
        if len(self.treeVars)>0:
            self.treeVars.update(self.getUsedVariables(self.cutsMC))
            self.treeVars.update(self.getUsedVariables(self.cutsData))
            self.treeVars.update(self.getUsedVariables(self.weightMC))
    
    
    def clone(self,**args):
        new = copy.copy(self)
        new.xTitle=""
        new.yTitle=""
        new.plotName=""
        new.opts=""
        new.treeVars=set()
        for arg in args:
            setattr(new,arg,args[arg])
        new.init()
        return new
        
    def getUsedVariables(self,cuts_weight):
        cuts_weight = cuts_weight.replace("&", " ")
        cuts_weight = cuts_weight.replace("*", " ")
        cuts_weight = cuts_weight.replace("/", " ")
        cuts_weight = cuts_weight.replace("+", " ")
        cuts_weight = cuts_weight.replace("-", " ")
        cuts_weight = cuts_weight.replace("|", " ")
        cuts_weight = cuts_weight.replace("(", " ")
        cuts_weight = cuts_weight.replace(")", " ")
        cuts_weight = cuts_weight.replace(">", " ")
        cuts_weight = cuts_weight.replace("<", " ")
        return cuts_weight.split(" ")

