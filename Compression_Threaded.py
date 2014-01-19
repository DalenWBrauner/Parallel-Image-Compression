"""
.                                   .
|   Compression_Threaded.py         |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *

"""
# Builtin libs
import math, time
from math import sqrt, cos, pi

# Required libs
from numpy import matrix, array
from scipy import ndimage as image

#
##
### Core functions:
def main():
    print "What is the filename?"
    print "Hints:"
    print "C:\Users\Dalen\Desktop\winter-wallpaper-24.png"
    print "C:\Users\Dalen\Desktop\\bird.png"
    UsersImage = image.imread(raw_input(''))
    if (UsersImage.shape[0] %8 != 0) or (UsersImage.shape[1] %8 != 0):
        raise TypeError("Requires an image whose size is a multiple of 8x8!")
    print "What level of image quality would you prefer? Please select an integer 1-25,"
    print "1 being the greatest image quality but least compressed."
    Quality = int(raw_input(''))
    NewImage = Compress(UsersImage,Quality)

def Compress(i,q):
    """Returns a compressed version of the image.
    The majority of this should be parallelized."""
    # 'i' Should be an Length*Width*4 array of RGB color values
