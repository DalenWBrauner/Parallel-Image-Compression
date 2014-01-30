"""
.                                   .
|   Decompression.py                |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *
"""
# Builtin libs
import time, pickle

# Required libs
from numpy import matrix, array
from scipy import ndimage as image, misc

# Custom libs
from array_handler import arraymap
from Compression import Calc_DCT

#
##
###
####
##### Core functions:
def main():
    filename = raw_input("What is the filename? ")
    if filename[-11:] != '.compressed':
        raise TypeError("Requires a .compressed file from Compression.py!")
    f = open(filename,'rb')
    data = pickle.load(f)
    f.close()
    quality = input("And what was the quality of compression? ")
    Decompress(data,filename[:-11],quality)
    
def Decompress(data,filename,quality):
    """Saves a decompressed version of the image."""
    tt = 0

    
    print "Seperating Blocks...",
    t0 = time.clock()
    R, G, B = Split_Blocks(data)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."

    
    print "De-Quantizing data...",
    t0 = time.clock()
    R_DQ = DeQuantize(R,quality)
    G_DQ = DeQuantize(G,quality)
    B_DQ = DeQuantize(B,quality)
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
###
####
##### Stepping-stone functions:

def Decode_Width(code):
    """Decodes a Run_Width-encoded list"""
    msg = []
    i = 0
    if code[-1] == chr(128) and code[-2] == chr(128):
        code = code[:-2]
    while i < len(code):
        if ord(code[i]) == 128:
            i += 1
            for num in xrange(ord(code[i])): msg.append(0)
        elif ord(code[i]) == 255:
            n = 255
            i += 1
            while ord(code[i]) == 255:
                n += 255
                i += 1
            msg.append(ord(code[i])-128+n)
        elif ord(code[i]) == 0:
            n = -255
            i += 1
            while ord(code[i]) == 0:
                n -= 255
                i += 1
            msg.append(ord(code[i])-128+n)
        else:
            msg.append(ord(code[i])-128)
        i += 1

    return msg

def Split_Blocks(data):
    """Decodes and sections the data into 3 arrays of 8x8 blocks"""
    shape = ord(data[0]), ord(data[1])
    code = data[2:].split( str(chr(128) + chr(128)) )
    code.pop()
    split = [[[[] for w in xrange(shape[1])] for l in xrange(shape[0])] for c in xrange(3)]
    pos = 0
    try:
        for block in code:
            decoded = Decode_Width(block)
            x = (pos / shape[1]) / shape[0]
            y = (pos / shape[1]) % shape[0]
            z =  pos % shape[1]
            split[x][y][z] = decoded
            pos += 1
    except IndexError:
        print pos
        raise IndexError
    return array(split)

def DeQuantize(data,Q):
    """Given a numpy array of zig-zagged and quantized lists "data" and quality level "Q",
    returns a numpy array of the same values in 8x8 matrices."""
    # Establishes the Quality Matrix and the Zigzag pattern
    Qtrx = matrix([[(1 + (x + y + 1)*Q) for x in xrange(8)] for y in xrange(8)])
    Zig = [(0,0),(0,1),(1,0),(2,0),(1,1),(0,2),(0,3),(1,2),(2,1),(3,0),
           (4,0),(3,1),(2,2),(1,3),(0,4),(0,5),(1,4),(2,3),(3,2),(4,1),(5,0),
           (6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6),(0,7),(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),
           (7,0),(7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),
           (7,3),(6,4),(5,5),(4,6),(3,7),(4,7),(5,6),(6,5),(7,4),(7,5),(6,6),(5,7),(6,7),(7,6),
           (7,7)]
    # Create a new array
    New = []
    # Unzigzaggs the list into a matrix
    for x in xrange(data.shape[0]):
        New.append([])
        for y in xrange(data.shape[1]):
            M = ([[0 for a in xrange(8)] for b in xrange(8)])
            for t in xrange(len(Zig)):
                Z0 = Zig[t][0]
                Z1 = Zig[t][1]
                try:
                    M[ Z0 ][ Z1 ] = data[x,y][t] * (Qtrx[ Z0 , Z1 ])
                except IndexError:
                    print '\nshape',data.shape
                    print 'x:',x
                    print 'y:',y
                    print 't:',t
                    print '\ndata[x]:',data[x]
                    print '\ndata[x,y]:',data[x,y]
                    print '\ndata[x,y][t]:',data[x,y][t]
            New[x].append(M)
    return array(New)

def Merge_Blocks(data):
    raise NotImplementedError
    return Red, Blu, Grn

if __name__ == "__main__":
    main()
