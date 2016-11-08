source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /mnt/t3nfs01/data01/shome/sdonato/CMSSW_8_0_19_patch2/src
eval `scramv1 runtime -sh`

echo $PWD
ls

cd /mnt/t3nfs01/data01/shome/sdonato/tth/DataMCplot
./DataMCplot.py --gc --batch
