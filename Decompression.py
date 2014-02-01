"""
.                                   .
|   Decompression.py                |
|   Written by Dalen W. Brauner     |
|   Status: "Finished"              |
*                                   *
"""
# Builtin libs
import time, pickle
from math import sqrt, cos, pi

# Required libs
from numpy import matrix, array
from scipy import misc

# Custom libs
from array_handler import arraymap

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
    R, G, B = Unpack_Blocks(data)
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

    
    print "Undoing DCTs...",
    t0 = time.clock()
    R_DCTs = arraymap(Undo_DCT, R_DQ, dtype=int, esize=2)
    G_DCTs = arraymap(Undo_DCT, G_DQ, dtype=int, esize=2)
    B_DCTs = arraymap(Undo_DCT, B_DQ, dtype=int, esize=2)
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

    
    misc.imsave((filename+'.png'),final_array)
    print "\nAll in all...",
    print "everything took",tt,"seconds."

#
##
###
####
##### Stepping-stone functions:

def Decode_Width(code, debugging=True):
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

    if debugging and len(msg) != 64:
        print "\nWhoa, this ain't 64 long...",msg
        print "It's off by",64-len(msg)
        print "Here's the original:",code,'\n'
    return msg

def Unpack_Blocks(data):
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
        print pos,x,y,z
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

def Undo_DCT(M):
    """Given a square numpy matrix "M", returns its DCT."""
    # Prevent modification of the original matrix
    M = M.copy()
    # Assure the matrix is square
    N, width = M.shape
    if N != width:  raise TypeError("DCT() requires matrix argument to be square")

    # Construct the Cosine Transform Matrix
    first = 1.0/sqrt(N)
    second = sqrt(2.0/N)
    third = 1.0/(2.0*N)
    C = matrix([[0 for j in xrange(N)] for i in xrange(N)],dtype='f')
    # Correct the first few values
    for i in xrange(N):
        C[0,i] = first
    # Calculate the rest
    for i in xrange(N-1):
        for j in xrange(N):
            C[i+1,j] = second * cos( (2*j+1) *(i+1) *pi *third)

    # Undo the Cosine Transform Matrix FIRST,
    M = (C.T * M * C).round(0)
    
    # THEN Scale input pixel values to be consistent with the JPEG algorithm
##    for i in xrange(N):
##        for j in xrange(N):
##            M[i,j] = M[i,j] + 128
            
    # Now we should have it!
    return M

def Merge_Blocks(A):
    """Given an N by M array of 8x8 matrices "A", returns the N*8 by M*8 array "MA" as if
    each slot in the array was split into 8x8, and each corresponding matrix value inserted
    into these new slots."""
    N = A.shape[1]
    M = A.shape[0]
    final = [[] for f in xrange(N*8)]
    for n in xrange(N):
        for y in xrange(8):
            for m in xrange(M):
                for x in xrange(8):
                    final[y + n*8].append(A[m,n][y,x])
    
    #raise NotImplementedError
    Merged = array(final)
    return Merged

if __name__ == "__main__":
    main()
