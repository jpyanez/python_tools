import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits import mplot3d
import jp_mpl as jplot
from scipy import interpolate, ndimage
from copy import deepcopy

def profile2D(image, pixel_size):

    image_dimensions = np.array(image.shape)*pixel_size # in mm
    #print 'Image dimensions', image_dimensions, ' (mm) '
    xaxis = np.linspace(0, 1, image.shape[1])*image_dimensions[1]
    yaxis = np.linspace(0, 1, image.shape[0])*image_dimensions[0]

    fig, ax = plt.subplots(2,2,
                           figsize = (12,12),
                           sharey='row',sharex='col',
                           gridspec_kw={'width_ratios':[1,4],
                                        'height_ratios':[4,1]})
    fig.delaxes(ax[1,0])

    xmax = image.max(axis=0)
    ax[1,1].plot(xaxis,xmax)

    ymax = image.max(axis=1)
    ax[0,0].plot(ymax, yaxis[::-1])

    ax[0,1].imshow(image, plt.cm.gray, 
                   aspect='auto',
                   extent = [0, image_dimensions[1], 0, image_dimensions[0]])

    plt.subplots_adjust(wspace=0, hspace=0)

    ax[0,0].set_ylabel('y (mm)')
    ax[1,1].set_xlabel('x (mm)')
    return fig

def profileContour(image, pixel_size):
    image_dimensions = np.array(image.shape)*pixel_size # in mm
    xaxis = np.linspace(0, 1, image.shape[1])*image_dimensions[1]
    yaxis = np.linspace(0, 1, image.shape[0])*image_dimensions[0]

    fig = plt.figure( figsize = (12,9))
    ax = fig.add_subplot(111)
    
    levels = np.linspace(noise, image.max(), 10)

    #### 
    cmap = plt.cm.viridis
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'Custom cmap', cmaplist, cmap.N)
    bounds = levels
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N) 
    #######
    
    c = ax.imshow(image, cmap=cmap, 
                  norm=norm, 
                  aspect='auto',
                  extent = [0, image_dimensions[1], 0, image_dimensions[0]])
    
    cf = ax.contour(xaxis, yaxis[::-1], image, 
                    levels = levels,
                    colors = 'white',
                    alpha = 0.5)

    plt.colorbar(c)
    
    plt.ylim(3, 7)
    plt.xlim(1.5, 8.5)
    
    return fig

def profile3D(image, pixel_size):
    image_dimensions = np.array(image.shape)*pixel_size # in mm
    xaxis = np.linspace(0, 1, image.shape[1])*image_dimensions[1]
    yaxis = np.linspace(0, 1, image.shape[0])*image_dimensions[0]
    
    fig = plt.figure(figsize=(18,16))
    ax = plt.axes(projection='3d')
    y = np.linspace(0, image_dimensions[0], image.shape[0])
    x = np.linspace(0, image_dimensions[1], image.shape[1])
    X, Y = np.meshgrid(x, y)
    ax.view_init(30, 40)
    ax.plot_surface(X, Y, image,
                   cmap='viridis')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_zlabel('Intensity')

    zoom = True
    if zoom:
        step= 6
        ax.set_xlim(3, 3+step)
        ax.set_ylim(2, 2+step)
    return fig

import re

def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """
    #print filename
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return np.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))
