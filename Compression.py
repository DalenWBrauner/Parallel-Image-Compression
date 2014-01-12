"""
.                                   .
|   Compression.py                  |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *

"""
# Builtin libs
import math, random
from math import sqrt, cos, pi

# Required libs
from numpy import matrix, array
from scipy import ndimage as image

# Custom libs
# N/A

def main():
##    UsersImage = image.imread(raw_input("What is the filename? "))
##    NewImage = Compress(UsersImage)
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

def Compress(i):
    """Returns a compressed version of the image."""
    Colors = Seperate_Color_Data(i)
    The_DCTs = map(DCT, Colors)
    return The_DCTs

def Seperate_Color_Data(i):
    """Returns an R, G and B matrix."""
    R, G, B = [], [], []
    for x in xrange(i.shape[0]):
        R.append([])
        G.append([])
        B.append([])
        for y in xrange(i.shape[1]):
            R[x].append(int(i[x,y][0]))
            G[x].append(int(i[x,y][1]))
            B[x].append(int(i[x,y][2]))
    return( matrix(R), matrix(G), matrix(B) )

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

main()
