"""
.                                   .
|   Compression.py                  |
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
### Core functions
def main():
    print "What is the filename?"
    print "Hints:"
    print "C:\Users\Dalen\Desktop\winter-wallpaper-24.png"
    print "C:\Users\Dalen\Desktop\\bird.png"
    UsersImage = image.imread(raw_input(''))
    if (UsersImage.shape[0] %8 != 0) or (UsersImage.shape[1] %8 != 0):
        raise TypeError("Requires an image whose size is a multiple of 8x8!")
    print "What level of image quality would you prefer?"
    print "Please select an integer 1-25, 1 being the greatest quality but least compressed."
    Quality = int(raw_input(''))
    NewImage = Compress(UsersImage,Quality)

def Compress(i,q):
    """Returns a compressed version of the image.
    The majority of this should be parallelized."""

    print "Seperating Colors...",
    t0 = time.clock()
    Colors = Split_RGB(i)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."

    print "Splitting the image into 8x8 blocks...",
    t0 = time.clock()
    # This is split into three to avoid excessive compound lists
    R_Blocks, G_Blocks, B_Blocks = map(Split_Blocks, Colors)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."

    print "Calculating DCTs...",
    t0 = time.clock()
    # Setup compound lists in an array-friendly format
    R_DCTs, G_DCTs, B_DCTs = [], [], []
    for i in xrange(R_Blocks.shape[0]):
        R_DCTs.append([])
        G_DCTs.append([])
        B_DCTs.append([])
        for j in xrange(R_Blocks.shape[1]):
            # Add DCT Matrices to said array-friendly lists
            R_DCTs[i].append(Calc_DCT(R_Blocks[i,j]))
            G_DCTs[i].append(Calc_DCT(G_Blocks[i,j]))
            B_DCTs[i].append(Calc_DCT(B_Blocks[i,j]))
    # Convert to integer-only arrays when finished!
    R_DCTs = array(R_DCTs,dtype='int')
    G_DCTs = array(G_DCTs,dtype='int')
    B_DCTs = array(B_DCTs,dtype='int')
    t1 = time.clock()
    print "took",(t1-t0),"seconds."

    print "Quantizing data...",
    t0 = time.clock()
    # Each '_DCTs' variable is now an array of 8x8 matricies, encompassing
    # the entire image for that respective color.
    R_Quantized = Quantize(R_DCTs,q)
    G_Quantized = Quantize(G_DCTs,q)
    B_Quantized = Quantize(B_DCTs,q)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."

    print "Applying Huffman codes..."
    t0 = time.clock()
    R_Final = Huffman(R_Quantized)
    G_Final = Huffman(G_Quantized)
    B_Final = Huffman(B_Quantized)
    t1 = time.clock()
    print "took",(t1-t0),"seconds."
    
##    final_product = ?
##    return final_product

def Split_RGB(i):
    """Returns an R, G and B matrix."""
    R, G, B, Alpha = i.swapaxes(0,2)
    return (matrix(R), matrix(G), matrix(B))

def Seperate_Color_Data2(i):
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

#
##
### Don't mind these, they're for debugging.

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
    
def Huffman(argument):
    raise NotImplementedError

main()
