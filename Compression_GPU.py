"""
.                                   .
|   Compression_GPU.py              |
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

# GPU libs
import pycuda.autoinit
import pycuda.gpuarray as gpuarray

# Custom libs
from array_handler import arraymap

#
##
### Core functions:
def main():
    print "What is the filename?"
    print "Win:"
    print "C:\Users\Dalen\Desktop\winter-wallpaper-24.png"
    print "C:\Users\Dalen\Desktop\\bird.png"
    print "Mint:"
    print "./winter-wallpaper-24.png"
    print "./bird.png"
    
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
    
    print "Seperating Colors...",
    ts = t0 = time.clock()
    Colors = Split_RGB(i)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."
    # 'Colors' should be a list of the Length*Width arrays for each color value
    
    print "Splitting the image into 8x8 blocks...",
    t0 = time.clock()
    R_Blocks, G_Blocks, B_Blocks = map(Split_Blocks, Colors)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."
    # Each '_Blocks' variable should be an array of 8x8 matricies, each containing
    # the respective R, G or B pixel data for that 8x8 portion of the image
    
    print "Calculating DCTs...",
    t0 = time.clock()
    R_DCTs = arraymap(Calc_DCT, R_Blocks, dtype=int, esize=2)
    G_DCTs = arraymap(Calc_DCT, G_Blocks, dtype=int, esize=2)
    B_DCTs = arraymap(Calc_DCT, B_Blocks, dtype=int, esize=2)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."
##    print '\n Sample before DCT:'
##    print R_Blocks[0,0]
##    print '\n Sample after DCT:'
##    print R_DCTs[0,0]
    # Each '_DCTs' variable should be an array of the DCTs of said 8x8 matrices
    
    print "Quantizing data...",
    t0 = time.clock()
    R_Quantized = Quantize(R_DCTs,q)
    G_Quantized = Quantize(G_DCTs,q)
    B_Quantized = Quantize(B_DCTs,q)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."
##    print 'R_Quantized\n',R_Quantized[0]
##    print 'G_Quantized\n',G_Quantized[0]
##    print 'B_Quantized\n',B_Quantized[0]
    # Each '_Quantized' variable should be an array of lists of each DCT
    # reorganized in a lossy, zigzag fashion
    
    print "Applying Run Length Algorithm...",
    t0 = time.clock()
    R_RunLen = arraymap(Run_Length, R_Quantized)
    G_RunLen = arraymap(Run_Length, G_Quantized)
    B_RunLen = arraymap(Run_Length, B_Quantized)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."
##    print 'R_Quantized\n',R_Quantized[0]
##    print 'R_RunLen\n',R_RunLen[0],'\n'
##    print 'G_Quantized\n',G_Quantized[0]
##    print 'G_RunLen\n',G_RunLen[0],'\n'
##    print 'B_Quantized\n',B_Quantized[0]   
##    print 'B_RunLen\n',B_RunLen[0]
    # Each '_RunLen' variable should be an array of compressed lists holding
    # tuples of each value and the following number of zeroes
    
    print "Applying Huffman codes..."
    t0 = time.clock()
    R_Final = Huffman(R_RunLen)
    G_Final = Huffman(G_RunLen)
    B_Final = Huffman(B_RunLen)
    tf = t1 = time.clock()
    print "took",(t1-t0),"seconds."

    print "The image has been compressed!"
    print "Hah, and it only took",(tf-ts),"seconds!"
    
##    final_product = ?
##    return final_product

#
##
### Stepping-stone functions:

def Split_RGB(i):
    """Returns an R, G and B matrix."""
    R, G, B, Alpha = i.swapaxes(0,2)
    return (matrix(R), matrix(G), matrix(B))

def Split_YUV(i):
    """Returns a Y', U and V matrix. (Unused)"""
    # Establish conversion constants
    C = (.299, .587, .114, -.14713, -.28886, .436, .615, -.51499, -.10001)
    # Prep YUV lists
    Y, U, V = [], [], []
    for x in xrange(i.shape[0]):
        Y.append([])
        U.append([])
        V.append([])
        for y in xrange(i.shape[1]):
            R = int(i[x,y][0])
            G = int(i[x,y][1])
            B = int(i[x,y][2])
            # Append to lists YUV
            Y[x].append( R*C[0] + G*C[1] + B*C[2])
            U[x].append( R*C[3] + G*C[4] + B*C[5])
            V[x].append( R*C[6] + G*C[7] + B*C[8])
    return( matrix(Y), matrix(U), matrix(V) )

def Split_Blocks(M):
    """Splits a Matrix into an array of 8x8 blocks"""
    h = M.shape[0]/8
    w = M.shape[1]/8
    blocks = [[] for q in xrange(w)]
    for y in xrange(w):
        for x in xrange(h):
            blocks[y].append(M[(x*8) : (x*8+8), (y*8) : (y*8+8)])
    A = array(blocks)
    return A

def Calc_DCT(M):
    """Given a square numpy matrix "M", returns its DCT."""
    # Assure the matrix is square
    N, width = M.shape
    if N != width:  raise TypeError("DCT() requires matrix argument to be square")

    # Calculate constants
    first = 1.0/sqrt(N)
    second = sqrt(2.0/N)
    third = 1.0/(2.0*N)
    
    # Create the Cosine Transform Matrix
    C = matrix([[0 for j in xrange(N)] for i in xrange(N)],dtype='f')
    # Correct the first few values
    for i in xrange(N):
        C[0,i] = first
    for i in xrange(N-1):
        for j in xrange(N):
            C[i+1,j] = second * cos( (2*j+1) *(i+1) *pi *third)

    # Scale input pixel values to be consistent with the JPEG algorithm
    for i in xrange(N):
        for j in xrange(N):
            M[i,j] = M[i,j] - 128
            
    # Calculate and round the DCT itself
    return (C * M * C.T).round(0)

def Quantize(A,Q):
    """Given a numpy array of 8x8 matrices "A" and quality level "Q", returns
    a numpy array of the same values in lists, zig-zagged and quantized."""
    # Establishes the Quality Matrix and the Zigzag pattern
    Qtrx = matrix([[(1 + (x + y + 1)*Q) for x in xrange(8)] for y in xrange(8)])
    Zig = [(0,0),(0,1),(1,0),(2,0),(1,1),(0,2),(0,3),(1,2),(2,1),(3,0),
           (4,0),(3,1),(2,2),(1,3),(0,4),(0,5),(1,4),(2,3),(3,2),(4,1),(5,0),
           (6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6),(0,7),(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),
           (7,0),(7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),
           (7,3),(6,4),(5,5),(4,6),(3,7),(4,7),(5,6),(6,5),(7,4),(7,5),(6,6),(5,7),(6,7),(7,6),
           (7,7)]
    # Creates a list to be returned as the new array
    New = []
    for x in xrange(8):
        New.append([])
        for y in xrange(8):
            # For every item in the 8x8 matrix, the respective quantized value is appended to Zag
            # This is done in 'zig-zag' order via the tuples in Zig
            M = A[x,y]
            Zag = []
            Zag = [ M[tup[0],tup[1]] / float(Qtrx[tup[0],tup[1]]) for tup in Zig]
            Zagg = map(int,Zag)
            New[x].append(Zagg)
    return array(New)

def Run_Length(values):
    """Given a list of values, returns a list of tuples with non-zero
    values and the number of zeroes that follow it in the original sequence"""
    new_list = []
    tup = [values[0],0]
    v = 1
    while v < len(values):
        if values[v] != 0:
            new_list.append(tuple(tup))
            tup = [values[v],0]
        else:
            tup[1] += 1
        v += 1
    new_list.append(tuple(tup))
    return new_list
                
def Huffman(argument):
    raise NotImplementedError               

#
##
### Debugging functions:

def Test_DCT():
    UsersImage = array([
    [140, 144, 147, 140, 140, 155, 179, 175],
    [144, 152, 140, 147, 140, 148, 167, 179],
    [152, 155, 136, 167, 163, 162, 152, 172],
    [168, 145, 156, 160, 152, 155, 136, 160],
    [162, 148, 156, 148, 140, 136, 147, 162],
    [147, 167, 140, 155, 155, 140, 136, 162],
    [136, 156, 123, 167, 162, 144, 140, 147],
    [148, 155, 136, 155, 152, 147, 147, 136]
    ])
    print Calc_DCT(UsersImage),'\n'
    
    UsersImage2 = array([
    [52, 55, 61,  66,  70,  61, 64, 73],
    [63, 59, 55,  90, 109,  85, 69, 72],
    [62, 59, 68, 113, 144, 104, 66, 73],
    [63, 58, 71, 122, 154, 106, 70, 69],
    [67, 61, 68, 104, 126,  88, 68, 70],
    [79, 65, 60,  70,  77,  68, 58, 75],
    [85, 71, 64,  59,  55,  61, 65, 83],
    [87, 79, 69,  68,  65,  76, 78, 94]
    ])
    print Calc_DCT(UsersImage2)
    
def Test_Quantize():
    DCT_Before = matrix([
    [ 92,   3,  -9,  -7,   3, -1,  0,  2],
    [-39, -58,  12, -17,  -2,  2,  4,  2],
    [-84,  62,   1, -18,   3,  4, -5,  5],
    [-52, -36, -10,  14, -10,  4, -2,  0],
    [-86, -40,  49,  -7,  17, -6, -2,  5],
    [-62,  65, -12,  -2,   3, -8, -2,  0],
    [-17,  14, -36,  17, -11,  3,  3, -1],
    [-54,  32,  -9,  -9,  22,  0,  1,  3]
    ])
    Qtrx = matrix([[(1 + (x + y + 1)*2) for x in xrange(8)] for y in xrange(8)])
    print Qtrx
    print DCT_Before
    DCT_Mid = DCT_Before.copy()
    for i in xrange(8):
        for j in xrange(8):
            # Obnoxiously, python always rounds down, even with negative numbers.
            # i.e. -39/5 = -8, while 39/5 = 7.
            DCT_Mid[i,j] /= float(Qtrx[i,j])
            DCT_Mid[i,j] = round(DCT_Mid[i,j])
    print '\n',DCT_Mid
    DCT_After = DCT_Mid.copy()
    for i in xrange(8):
        for j in xrange(8):
            DCT_After[i,j] *= Qtrx[i,j]
    print '\n',DCT_After
    QQ = Quantize(array([[DCT_Before for x in xrange(8)] for x in xrange(8)]), 2)
    print '\nCompare the following, the second being in zigzag order\n',DCT_Mid
    print QQ[0,0]
    print 'Ultimately, the important thing is the number of 0s.'

def Test_Run_Length():
    samplelist1 = [30, 0, -7, -12, -8, -1, 0, 1, 6, -5, -7, -3, 0, -1, 0, 0, 0, -1,
                  0, -3, -4, -1, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0]
    samplelist2 = [0, 0, -7, -12, -8, -1, 0, 1, 6, -5, -7, -3, 0, -1, 0, 0, 0, -1,
                  0, -3, -4, -1, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0]
    samplelist3 = [30, 0, -7, -12, -8, -1, 0, 1, 6, -5, -7, -3, 0, -1, 0, 0, 0, -1,
                  0, -3, -4, -1, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -1,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 7, 0]
    newlist1 = Run_Length(samplelist1)
    newlist2 = Run_Length(samplelist2)
    newlist3 = Run_Length(samplelist3)
    print "Before:\n",samplelist1
    print "After:\n",newlist1
    print "No. Values Before:",len(samplelist1)
    print "No. Values After:",(2*len(newlist1))
    print '\n'
    print "Before:\n",samplelist2
    print "After:\n",newlist2
    print "No. Values Before:",len(samplelist2)
    print "No. Values After:",(2*len(newlist2))
    print '\n'
    print "Before:\n",samplelist3
    print "After:\n",newlist3
    print "No. Values Before:",len(samplelist3)
    print "No. Values After:",(2*len(newlist3))

if __name__ == "__main__":
    main()
    #Test_DCT()
    #Test_Quantize()
    #Test_Run_Length()
