"""
Run me like this:
python ./plotter.py <path/pcaChain1> <path/pcaChain2> <"show" or the name of the file to save> <configurations>
python ./movieMaker.py data/1abs data/1abs2 1abs2ch.pdf 30 44 58

If you pass only the first two argument then I will
plot the  0-th configuration.
"""

#============ parameters ===============
# Plot
randomSeed = 11;

dotSize = None; #if None then optimal size will be found
lineSize = None; # = '#ee0000'; if None then optimal size will be found

dotColor = "#cc0000"; #if None then will be random
lineColor = "#660000"; #if None then will be random
dotColor2 = "#0066cc"; #if None then will be random
lineColor2 = "#00264d"; #if None then will be random

dotHueDispersion = 0.05; #[0,1];
dotSaturationDispersion = 0.1; #[0,1];
dotVolumeDispersion = 0.1; #[0,1];

# Axes
elevation = None;
azimut = None;
axisOnOff ='on';
#=======================================

import sys
sys.path.append('Plotter_lib/');

import matplotlib.pyplot as plt
import Polymer
import EqualAxes
import Color
import sys
import random

random.seed(randomSeed);

if(len(sys.argv)<3):
    print(__doc__);
    exit();
fileName = sys.argv[1];
fileName2 = sys.argv[2];
#fileName = "/Users/annsi118/Documents/Git_projects/PCMC/Projects/MonteCarlo2chains/results/Configurations/0confR.dat";
#fileName2 = "/Users/annsi118/Documents/Git_projects/PCMC/Projects/MonteCarlo2chains/results/Configurations/0confR2.dat";
polymer = Polymer.Polymer(fileName+".pca");
polymer2 = Polymer.Polymer(fileName2+".pca");

fig = plt.figure()
ax = fig.gca(projection='3d');
ax.set_aspect('equal');
eqAx = EqualAxes.EqualAxes(ax);

if(len(sys.argv)<5):
    confNum = 0;
    eqAx.push(polymer.getX(confNum),polymer.getY(confNum),polymer.getZ(confNum));
    eqAx.push(polymer2.getX(confNum),polymer2.getY(confNum),polymer2.getZ(confNum));
    dotSmartColors = Color.arrayWithSmartColors(polymer.getChainLenght(0),
	    dotHueDispersion, dotSaturationDispersion, dotVolumeDispersion, dotColor);
    dotSmartColors2 = Color.arrayWithSmartColors(polymer2.getChainLenght(0),
	    dotHueDispersion, dotSaturationDispersion, dotVolumeDispersion, dotColor2);
    polymer.plot(confNum, eqAx, dotSize, lineSize, dotSmartColors, lineColor);
    polymer2.plot(confNum, eqAx, dotSize, lineSize, dotSmartColors2, lineColor2);
    
else:
    for i in range(4,len(sys.argv)):
	confNum = int(sys.argv[i]);
	print('Chain %s has %i atoms.' % (sys.argv[i], polymer.getN(confNum)));
	eqAx.push(polymer.getX(confNum),polymer.getY(confNum),polymer.getZ(confNum));
	eqAx.push(polymer2.getX(confNum),polymer2.getY(confNum),polymer2.getZ(confNum));

	
    for i in range(4,len(sys.argv)):
	confNum = int(sys.argv[i]);
	dotSmartColors = Color.arrayWithSmartColors(polymer.getChainLenght(0),
		dotHueDispersion, dotSaturationDispersion, dotVolumeDispersion, dotColor);
	dotSmartColors2 = Color.arrayWithSmartColors(polymer2.getChainLenght(0),
		dotHueDispersion, dotSaturationDispersion, dotVolumeDispersion, dotColor2);
	polymer.plot(confNum, eqAx, dotSize, lineSize, dotSmartColors, lineColor);
	polymer2.plot(confNum, eqAx, dotSize, lineSize, dotSmartColors2, lineColor2);
#	polymer.smartColorPlot(confNum,ax, axMaxRange, "#002255");
#	polymer.happyPlot(confNum,ax, axMaxRange);
#	polymer.plotOld(confNum, ax);
	

eqAx.set();
ax.view_init(elevation, azimut);
plt.axis(axisOnOff);

if(len(sys.argv)<4 or sys.argv[3] == 'show'):
    plt.show();
else:
    fig.savefig(sys.argv[3]);
