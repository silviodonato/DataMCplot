import ROOT
import copy
import os.path 

class DatasetClass(object):
    def __init__(self, fileName=""):
        self.fileName = fileName
    def loadTree(self):
        if hasattr(self,"tree"):
            print "Check the group definition: you are using a sample two times!"
        if not os.path.isfile(self.fileName):  raise Exception("File %s does not exist."%self.fileName) 
        self.tfile = ROOT.TFile(self.fileName)
        self.tree = self.tfile.Get("tree")
        print "Getting tree from ",self.fileName #," id=",id(self.tree)
        assert(type(self.tree)==ROOT.TTree)
        assert(self.tree.GetEntries()>0)
    def closeFile(self):
        self.tfile.Close()

class DatasetMCClass(DatasetClass):
    def __init__(self, xsec=1., fileName=""):
        DatasetClass.__init__(self, fileName)
        self.xsec = xsec
    def loadTree(self):
        DatasetClass.loadTree(self)
        self.count = self.getCount()
        print self.fileName,self.count
    def getCount(self):
        return self.tfile.Get("Count").GetBinContent(1)
    def setSingleEventWeight(self,lumi):
        self.singleEventWeight = lumi * self.xsec / self.count
        

class DatasetDataClass(DatasetClass):
    def __init__(self, lumi=1., fileName=""):
        DatasetClass.__init__(self, fileName)
        self.lumi = lumi #pb

class DatasetDataDrivenClass(DatasetClass):
    def __init__(self, weight=1., fileName=""):
        DatasetClass.__init__(self, fileName)
        self.weight = weight
    def loadTree(self):
        DatasetClass.loadTree(self)
        self.tree.GetEntry(0)
        self.lumi = float(self.tree.luminosity)
        print self.fileName
    def setSingleEventWeight(self,lumi):
        self.singleEventWeight = lumi / self.lumi
        print "self.lumi:",self.lumi
        

class GroupClass():
    def __init__(self, color=3, latexName="", samples=[], groupType="data"):
        self.color = color
        self.latexName = latexName
        self.name = filter(str.isalnum, self.latexName)
        self.samples = samples
        self.type = groupType
        if not groupType in ["data","signal","background","backgroundFromData"]:
            raise Exception('In group %s, the groupType is %s but it must be among ["data","signal","background","backgroundFromData"]')

class HistogramClass():
    def __init__(self, var="", nbins=1, xmin=0, xmax=1, folder=".", weightMC="1.", cutsMC="1", cutsData="1", treeVars=set(), xTitle="", yTitle="", plotName="", opts="", normalized=False, blinded=False, category="", region=""):
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
        self.normalized =normalized
        self.blinded =blinded
        self.category =category
        self.region =region
        self.init()
        
    def init(self):
        if self.xTitle == "": self.xTitle = self.var
        if self.plotName=="":
            self.plotName = filter(str.isalnum, self.xTitle)
            self.plotName = self.plotName.replace("GeV","")
        bin_size = 1.*(self.xmax-self.xmin)/self.nbins
        if self.yTitle == "": self.yTitle = "Events/"+str(bin_size)
        if self.opts == "": self.opts = "HIST goff"
        if len(self.treeVars)>0:
            self.treeVars.update(self.getUsedVariables(self.cutsMC))
            self.treeVars.update(self.getUsedVariables(self.cutsData))
            self.treeVars.update(self.getUsedVariables(self.weightMC))
        category = self.category.split("_")
        
    def clone(self,**args):
        new = copy.copy(self)
        new.xTitle=""
	new.plotName=""
	new.yTitle = ""
	new.opts =""
	'''
	if new.xTitle== new.var: new.xTitle=""
        if new.plotName== filter(str.isalnum, new.xTitle): new.plotName=""
        bin_size = 1.*(new.xmax-new.xmin)/new.nbins
        if new.yTitle == "Events/"+str(bin_size): new.yTitle = ""
        if new.opts == "HIST goff" : new.opts =""
	'''
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

