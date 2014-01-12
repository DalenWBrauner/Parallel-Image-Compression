# Builtin libs
import math, random
from math import sqrt, cos, pi

# Required libs
from numpy import matrix, array
from scipy import ndimage as image
# Custom libs
# N/A

def main():
    ##UsersImage = image.imread(raw_input("What is the filename? "))
    ##print Compress(UsersImage)
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
    return DCT(UsersImage)

def Compress(i):
    """Returns a compressed version of the image."""
    final_product = False
    Colors = Seperate_Color_Data(i)    
    The_DCTs = map(DCT, Colors)
    Quan = map(Quantize(2), The_DCTs)
    return final_product

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
    # Create the Cosine Transform Matrix
    C = matrix([[0 for i in xrange(8)] for i in xrange(8)],dtype='f')
    for i in xrange(8): C[0,i] = 1.0/sqrt(8)
    for i in xrange(7):
        for j in xrange(8):
            C[i+1,j] = .5 * cos( (2*j+1) *(i+1) *pi *.0625)
            
    # Calculate and round the DCT itself
    dct = C * M * C.T
    return dct.round(0)

#def 

a = main()
for mat in a:
    print mat
