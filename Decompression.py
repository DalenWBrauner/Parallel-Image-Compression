"""
.                                   .
|   Decompression.py                |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *

"""
# Builtin libs
import time

# Required libs
from numpy import matrix, array
from scipy import ndimage as image, misc

# Custom libs
from array_handler import arraymap
from Compression import Calc_DCT, Decode_Width

#
##
### Core functions:
def main():
    filename = raw_input("What is the filename? ")
    if filename[7:] != 'compression':
        raise TypeError("Requires a .compression file from Compression.py!")
    f = open(filename,'r')
    Data = f.read()
    f.close()
    Decompress(Data)

def Decompress(data):
    """Saves a decompressed version of the image."""

    print "Seperating Blocks...",
    t0 = time.clock()
    R, G, B = Split_Blocks(data)
    


#
##
### Stepping-stone functions:

def Split_Blocks(data):
    
    
    return Red, Blu, Grn
