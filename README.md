# Data MC plot

This code is a simple script that plots a generic data/MC plot.
It was originally developed for the search for the fully hadronic ttH, but it can be used for any analysis.
The histograms, datasets, cross-sections, colors, integrated luminosity, (...) are defined in a config file in the configs folder.
To get started:
~~~
cp configs/config_defaults.py configs/myConfigFile.py
~~~
and then edit your config file (myConfigFile.py) according your needs.

To run the code:
~~~
python DataMCplot.py -c configs/myConfigFile.py
~~~

This code allows you to get the histograms both using the TTree::Draw function (very fast) and looping over the events (slow but very flexible). 
In the latter case, you just need to define a user function taking TTree as input and returning a float.

Example:
def myFunction ( tree ):
    pt1 = tree.jets_pt[0]
    pt2 = tree.jets_pt[0]
    return pt1+pt2

# Grid-control

You can submit multiple jobs in parallel using grid-control.
The first step is the creation of a ".csv" with the jobs list:
~~~
./makeParametersCSV.py configs/####YOURCONFIGURATION#####.py
~~~
Then, you can submit the jobs with the command:
~~~
#if needed, delete the "plots" folder
./grid-control/go.py -c gc.conf  -cG
~~~
