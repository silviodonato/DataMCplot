# Data MC plot

This code is a simple script that plot a generic data/MC plot.
It was originally developed for the search for the fully hadronic ttH, but it can be used for any analysis.
The histograms, datasets, cross-sections, colors, integrated luminosity, (...) are defined in a config file in the configs folder.
To get started:
~~~
cp configs/config_defaults.py configs/myConfigFile.py
~~~
and then you can modify your config file (myConfigFile.py).

To run the code:
~~~
python DataMCplot.py -c configs/myConfigFile.py
~~~

This code allows you to get the histograms using the TTree::Draw function (very fast) and looping a user defined function over the events (slow but very flexible).
