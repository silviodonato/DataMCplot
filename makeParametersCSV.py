#!/usr/bin/python
import sys, os

njobs = 100
f = open('parameters.csv', 'w')

configs = sys.argv[1:]
os.system("ln "+configs[0]+" tempForCSV.py")
import tempForCSV
print "config;histo_total;histo_i"
f.write("config;histo_total;histo_i")
for config in configs:
    os.system("rm -f tempForCSV.py")
    os.system("ln "+config+" tempForCSV.py")
    reload(tempForCSV)
    counter = 0
    for histo in tempForCSV.histos:
        print "%s;%s;%s"%(config,njobs,counter)
        f.write("%s;%s;%s\n"%(config,njobs,counter))
        counter+=1

