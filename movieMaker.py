"""\
Run it like this:
python ./movieMaker.py <path/pcaFileIn> <increment> <gif/mp4> <path/fileOut>
python ./movieMaker.py 5dn7 3 gif movie

If you pass only the first (and second) argument then
no file will be generated, but everything will be 
showen on the screen.

!!!
For saving option you need additional packages which
are not included in matplotlib.

For saving gif imagemagick pack is needed.
For saving mp4 ffmpeg pack is needed.
"""
#============ parameters ===============
# Video
fps = 3;
dpi = 250;
frames = None; #number of frames, defailt = all frames

# Plot
dotSize = 20; #if None then optimal size will be found
lineSize = 1; #if None then optimal size will be found

dotColor = '#006699'; #if None then random color
lineColor = '#c21734'; # = '#ee0000'; if None then random color

dotHueDispersion = 0.02; #[0,1];
dotSaturationDispersion = 0.5; #[0,1];
dotVolumeDispersion = 0.2; #[0,1];


# Axes
elevation = None;
azimut = None;
axisOnOff ='off';
#=======================================
import sys
sys.path.append('Plotter_lib/');

import matplotlib.pyplot as plt
import Polymer
import EqualAxes
import Color
import math
import matplotlib.animation as animation


def update(i, increment):
	confNum = increment+(i-1)*increment;
	plt.cla();
	print('Chain %s has %i atoms.' % (confNum,polymer.getN(confNum)));
    
    #axMaxRange=eqAx.findMaxRange();
	
	polymer.plot(confNum, eqAx, dotSize, lineSize, dotSmartColors, lineColor);
#	polymer.smartColorPlot(confNum,ax,800/dotSize, dotColor, lineColor);
	eqAx.set();
	ax.view_init(elevation, azimut);
	plt.axis(axisOnOff);

if(len(sys.argv)<2):
    print(__doc__);
    exit();

fileNameIn = sys.argv[1];
polymer = Polymer.Polymer(fileNameIn+".pca");
dotSmartColors = Color.arrayWithSmartColors(polymer.getChainLenght(0),
		dotHueDispersion, dotSaturationDispersion, dotVolumeDispersion, dotColor);
fig = plt.figure()
fig.set_size_inches(3, 3, True)
ax = fig.gca(projection='3d');
ax.set_aspect('equal');
eqAx = EqualAxes.EqualAxes(ax);

#first frame
eqAx.push(polymer.getX(0),polymer.getY(0),polymer.getZ(0));
eqAx.set();
ax.view_init(elevation, azimut);
plt.axis(axisOnOff);

increment = 1;

#if pass increment
if(len(sys.argv)>2):
    increment = int(sys.argv[2]);
    if(increment < 1):
	increment = 1;
if(frames==None):
    frames =int(math.ceil(polymer.getNumChains()/float(increment)));
    print("Number of frames: %s."%frames);
anim = animation.FuncAnimation(fig, update,
		    frames=frames,
		    interval=1000/fps,
		    fargs = (increment,),
		    repeat = False
		    );

#if no saving
if(len(sys.argv)<4):
    plt.show();

#if save
else:
    extention = sys.argv[3];
    fileName=fileNameIn[:-3];
    fileNameOut=fileName +extention;
    
    #if pass fileNameOut
    if(len(sys.argv)>4):
	fileNameOut = sys.argv[4] +"."+ extention;
    
    if(sys.argv[3]=='gif'):
	writer = animation.ImageMagickFileWriter(fps=fps);
    if(sys.argv[3]=='mp4'):
	writer = animation.FFMpegWriter(fps=fps);
	
    anim.save(fileNameOut, writer=writer, dpi=dpi);
    print("File %s was successfully generated!" % fileNameOut);
