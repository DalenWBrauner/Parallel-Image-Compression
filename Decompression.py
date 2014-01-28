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
    if filename[-11:] != '.compressed':
        raise TypeError("Requires a .compressed file from Compression.py!")
    f = open(filename,'r')
    Data = f.read()
    f.close()
    Decompress(Data,filename[:-11])

def Decompress(data,filename):
    """Saves a decompressed version of the image."""

    print "Seperating Blocks...",
    t0 = time.clock()
    R, G, B = Split_Blocks(data)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."

    print "Decoding Widths...",
    t0 = time.clock()
    R_Decoded = arraymap(Decode_Width, R)
    G_Decoded = arraymap(Decode_Width, G)
    B_Decoded = arraymap(Decode_Width, B)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."
    
    print "De-Quantizing data...",
    t0 = time.clock()
    R_DQ, G_DQ, B_DQ = map(DeQuantize, (R_Decoded, G_Decoded, B_Decoded))
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."

    print "Calculating DCTs...",
    t0 = time.clock()
    R_DCTs = arraymap(Calc_DCT, R_DQ, dtype=int, esize=2)
    G_DCTs = arraymap(Calc_DCT, G_DQ, dtype=int, esize=2)
    B_DCTs = arraymap(Calc_DCT, B_DQ, dtype=int, esize=2)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."

    print "Merging 8x8 blocks...",
    t0 = time.clock()
    R_Merged, G_Merged, B_Merged = map(Merge_Blocks, (R_DCTs, G_DCTs, B_DCTs))
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."

    print "Rearranging Data...",
    t0 = time.clock()
    final_array = array([R_Merged, G_Merged, B_Merged]).swapaxes(0,2)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."

    misc.imsave(filename,final_array)
    print "\nAll in all...",
    print "everything took",tt,"seconds."


#
##
### Stepping-stone functions:

def Split_Blocks(data):
    raise NotImplementedError    
    return Red, Blu, Grn

def DeQuantize(data):
    raise NotImplementedError    
    return Red, Blu, Grn

def Merge_Blocks(data):
    raise NotImplementedError    
    return Red, Blu, Grn

#
##
### Debugging functions:

if __name__ == "__main__":
    main()
