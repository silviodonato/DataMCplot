source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /mnt/t3nfs01/data01/shome/sdonato/CMSSW_8_0_19_patch2/src
eval `scramv1 runtime -sh`
which python

echo $PWD
ls

echo "###### job parameters #######"
echo $config 
echo $histo_total
echo $histo_i
echo "#############################"

cd /mnt/t3nfs01/data01/shome/sdonato/tth/DataMCplot

echo "config="$config" histo_total="$histo_total" histo_i="$histo_i" ./DataMCplot.py --gc --batch"
config=$config histo_total=$histo_total histo_i=$histo_i ./DataMCplot.py --gc --batch
