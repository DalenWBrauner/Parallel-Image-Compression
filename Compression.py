"""
.                                   .
|   Compression.py                  |
|   Written by Dalen W. Brauner     |
|   Status: "Finished"              |
*                                   *
"""
# Builtin libs
import time, pickle
from math import sqrt, cos, pi

# Required libs
from numpy import matrix, array
from scipy import ndimage as image

# Custom libs
from array_handler import arraymap
#from Decompression import Decode_Width

#
##
###
####
##### Core functions:
def main():
    print "What is the filename?"
    print "Windows:"
    print "winter-wallpaper-24.png"
    print "bird.png"
    print "Linux Mint:"
    print "./winter-wallpaper-24.png"
    print "./bird.png"
    
    UsersImage = image.imread(raw_input(''))
    if (UsersImage.shape[0] %8 != 0) or (UsersImage.shape[1] %8 != 0):
        raise TypeError("Requires an image whose size is a multiple of 8x8!")
    print "What level of image quality would you prefer?\nPlease select an integer 1-25,"
    print "1 being the greatest image quality but least compressed."
    Quality = int(raw_input(''))
    Compress(UsersImage,Quality)

def Compress(i,q):
    """Saves a compressed version of the image.
    The majority of this should be parallelized."""
    # 'i' Should be an Length*Width*4 array of RGB color values
    tt = 0

    
    print "Seperating Colors...",
    t0 = time.clock()
    Colors = Split_RGB(i)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."
    # 'Colors' should be a list of the Length*Width arrays for each color value

    
    print "Splitting the image into 8x8 blocks...",
    t0 = time.clock()
    R_Blocks, G_Blocks, B_Blocks = map(Split_Blocks, Colors)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."
    # Each '_Blocks' variable should be an array of 8x8 matricies, each containing
    # the respective R, G or B pixel data for that 8x8 portion of the image

    
    print "Calculating DCTs...",
    t0 = time.clock()
    R_DCTs = arraymap(Calc_DCT, R_Blocks, dtype=int, esize=2)
    G_DCTs = arraymap(Calc_DCT, G_Blocks, dtype=int, esize=2)
    B_DCTs = arraymap(Calc_DCT, B_Blocks, dtype=int, esize=2)
    t1 = time.clock()
    tt += (t1-t0)
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
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."
##    print 'R_Quantized\n',R_Quantized[0]
##    print 'G_Quantized\n',G_Quantized[0]
##    print 'B_Quantized\n',B_Quantized[0]
    # Each '_Quantized' variable should be an array of lists of each DCT
    # reorganized in a lossy, zigzag fashion


    print "Applying Run Width Algorithm...",
    t0 = time.clock()
    R_RunW = arraymap(Run_Width, R_Quantized)
    G_RunW = arraymap(Run_Width, G_Quantized)
    B_RunW = arraymap(Run_Width, B_Quantized)
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."
    # Each '_Quantized' variable should be an array of Run_Width() strings


    print "Saving to file...",
    t0 = time.clock()
    # Original
    #f = open(str(time.time())+'.compressed','w')
    #Write_To(R_RunW, G_RunW, B_RunW, f.write)
    
    # Pickle the array
    #f = open(str(time.time())+'.compressed','wb')
    #pickle.dump((R_RunW, G_RunW, B_RunW), f)
    
    # Pickle the string
    O = appendablestring()
    f = open(str(int(time.time()*10))+'.compressed','wb')
    Write_To(q, R_RunW, G_RunW, B_RunW, O.append)
    pickle.dump(O.gimmie(), f)
    
    f.close()
    t1 = time.clock()
    tt += (t1-t0)
    print "took",(t1-t0),"seconds."
    # Hark! Our file hath been saved!
    print "\nAll in all...",
    print "everything took",tt,"seconds."

#
##
###
####
##### Stepping-stone functions:

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

    # Calculate the DCT
    M = (C * M * C.T).round(0)

    # Scale pixel values to be consistent with JPEG algorithm
    M[0,0] -= 1024
    return M

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
    for x in xrange(A.shape[0]):
        New.append([])
        for y in xrange(A.shape[1]):
            # For each item in the 8x8, the respective quantized value is appended to Zag
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

def Run_Width(values, debugging=True):
    """Given a list of values, returns a string of those values as characters,
    with the number of zeroes that follow each value as a character after.
    Values are re-incrimented by 128 so the majority of values are chr()-
    -compatable."""
    width = ''            
    v = 0
    z = 0
    try:
        while v < len(values):
            val = values[v] + 128
            if val == 128:
                z += 1
            else:
                # Add zeroes-character before adding other characters
                if z != 0:
                    width += chr(128)
                    width += chr(z)
                    z = 0

                # Check if the value is out of range, and continue
                # to add the appropriate character and amount to the
                # value until it is finally in range.
                if val >= 255:
                    while val >= 255:
                        width += chr(255)
                        val -= 255
                elif val <= 0:
                    while val <= 0:
                        width += chr(0)
                        val += 255

                # Finally: Add the character.
                width += chr(val)
            v += 1

        # If there are still zeroes to account for after exiting the loop...
        if z != 0:
            width += chr(128)
            width += chr(z)

    # Just in case something went wrong:
    except ValueError:
        print width
        print values[v],val
        print values
        err = "Run_Width Error: " + str(values[v]+128) + " not chr()able."
        raise ValueError(err)

    # To help make sure everything is in working order:
    if debugging:
        if len(values) != 64:
            print "Uhh, len(values) != 64."
            print len(values),values
        
##        decoded = Decode_Width(width)
##        if len(decoded) != len(values):
##               print "Run_Width and Decode_Width aren't getting along!"
##               print len(values),values
##               print len(decoded),decoded
##               print len(values) - len(decoded)

    # \x80\x80 Is used to split on prior to decoding the final string               
    return width + chr(128) + chr(128)

def Write_To(Q, Red, Grn, Blu, write):
    """Given RGB and a file's write function, writes appropriate headers and
    the contents of the array to the file."""
    L, W = Red.shape
    write(chr(Q))
    write(chr(L))
    write(chr(W))
    arraymap(write,Red)
    arraymap(write,Grn)
    arraymap(write,Blu)

#
##
####
##### Helper functions:

class appendablestring(object):
    """For continuing usage of arraymap. The goal of this object is to provide a function that
    serves to add the contents of a single argument to a string, similar to appending to a list.

    Before this object existed, we simply wrote to a file instead. This worked fine, until we
    discovered writing to a file added additional characters that showed up when loading.

    This is not the ideal approach."""
    def __init__(self):
        self._string = ''
        
    def append(self,stuff):
        if type(stuff) != str:
            try:
                for thing in stuff:
                    self.append(thing)
            except:
                err = "You can only append strings to me, not "+str(type(stuff))+"!"
                raise TypeError(err)
        elif type(stuff) == type(''):
            self._string += stuff
        else:
            print 'Um...?'
        
    def gimmie(self):
        return self._string

def printit(thing):
    """This is for passing 'print' to map or arraymap."""
    print thing

if __name__ == "__main__":
    main()
