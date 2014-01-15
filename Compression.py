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

def main():
    UsersImage = image.imread(raw_input("What is the filename? "))
    print "...file read!"
    if (UsersImage.shape[0] %8 != 0) or (UsersImage.shape[1] %8 != 0):
        raise TypeError("Requires an image whose size is a multiple of 8x8!")
    NewImage = Compress(UsersImage)

def Compress(i):
    """Returns a compressed version of the image.
    The majority of this should be parallelized."""
    Colors = Split_RGB(i)
    # This is split into three to avoid excessive compound lists
    R_Blocks, G_Blocks, B_Blocks = map(Split_Blocks, Colors)
    R_DCTs = map(DCT, R_Blocks)
    G_DCTs = map(DCT, G_Blocks)
    B_DCTs = map(DCT, B_Blocks)
    
##    Quan = map(Quantize, The_DCTs)
##    print "Quan"
##    print Quan,"\n"
##    
##    final_product = Quan
##    return final_product
        
    return (R_DCTs, G_DCTs, B_DCTs)

def Split_RGB(i):
    """Returns an R, G and B matrix."""
    X, Y, Z = i.shape
    R, G, B, trash = i.reshape((Z, X, Y))
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
    blocks = numpy.array([[0 for p in xrange(w)] for q in xrange(h)])
    for y in xrange(h):
	for x in xrange(w):
		blocks[x,y] = M[ (x*8) : (x*8+8), (y*8) : (y*8+8) ]
    return blocks

def DCT(M):
    """Given a numpy matrix "M", returns the DCT."""
    # Assure the matrix is square
    N, width = M.shape
    if N != width:  raise TypeError("DCT() requires matrix argument to be square")

    # Calculate constants
    first = 1.0/sqrt(N)
    second = sqrt(2.0/N)
    third = 1.0/(2.0*N)
    
    # Create the Cosine Transform Matrix
    C = matrix([[0 for i in xrange(N)] for i in xrange(N)],dtype='f')
    for i in xrange(N): C[0,i] = first
    for i in xrange(N-1):
        for j in xrange(N):
            C[i+1,j] = second * cos( (2*j+1) *(i+1) *pi *third)

    # Scale input pixel values to be consistent with the JPEG algorithm
    for i in xrange(N):
        for j in xrange(N):
            M[i,j] = M[i,j] - 128
            
    # Calculate and round the DCT itself
    return (C * M * C.T).round(0)

def Quantize(M):
    return M

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
    for mtrx in DCT(UsersImage):
        print mtrx

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
    for mtrx in DCT(UsersImage2):
        print mtrx

main()
