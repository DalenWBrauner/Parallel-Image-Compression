# Required libs
from numpy import matrix, array

# Custom libs
from array_handler import arraymap
from Compression import *
from Decompression import *

#
##
###
####
##### Compression.py

def Test_DCT():
    print 'Test_DCT()\n'
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
    print UsersImage
    print Calc_DCT(UsersImage)
    print Calc_DCT(Calc_DCT(UsersImage)),'\n'
    
    UsersImage = array([
    [52, 55, 61,  66,  70,  61, 64, 73],
    [63, 59, 55,  90, 109,  85, 69, 72],
    [62, 59, 68, 113, 144, 104, 66, 73],
    [63, 58, 71, 122, 154, 106, 70, 69],
    [67, 61, 68, 104, 126,  88, 68, 70],
    [79, 65, 60,  70,  77,  68, 58, 75],
    [85, 71, 64,  59,  55,  61, 65, 83],
    [87, 79, 69,  68,  65,  76, 78, 94]
    ])
    print UsersImage
    print Calc_DCT(UsersImage)
    print Calc_DCT(Calc_DCT(UsersImage)),'\n'

    UsersImage = array([
    [100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [100, 100, 100, 100, 100, 100, 100, 100]
    ])
    print UsersImage
    print Calc_DCT(UsersImage)
    print Calc_DCT(Calc_DCT(UsersImage)),'\n'
    
def Test_Quantize():
    print 'Test_Quantize()\n'
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
    QQ = Quantize(array([[DCT_Before for x in xrange(11)] for x in xrange(11)]), 2)
    print '\nCompare the following, the second being in zigzag order\n',DCT_Mid
    print QQ[0,0]
    print 'Ultimately, the important thing is the number of 0s.'
    print 'This is the sample at [9,9]:\n',QQ[9,9]

def Test_Run_Length():
    print 'Test_Run_Length()\n'
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

def Test_Run_Width():
    print 'Test_Run_Width()\n'
    def test(sample):
        Ws = Run_Width(sample)
        Ds = Decode_Width(Ws)
        L = len(Ws)
        print sample
        print "Results in length",L,"string:",Ws
        if L > 64:
            print "(This expanded! By",(L-64),"characters!)"
        print "Which translates to:\n",Ds
        print "(They are",
        if sample != Ds:
            print "not",
        print "the same.)\n"
        
    sam1 = [30, 0, -7, -12, -8, -1, 0, 1, 6, -5, -7, -3, 0, -1, 0, 0, 0, -1, 0, -3, -4, -1, 4,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sam2 = [0, 0, -7, -12, -8, -1, 0, 1, 6, -5, -7, -3, 0, -1, 0, 0, 0, -1, 0, -3, -4, -1, 4,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sam3 = [30, 0, -7, -12, -8, -1, 0, 1, 6, -5, -7, -3, 0, -1, 0, 0, 0, -1, 0, -3, -4, -1, 4,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
    sam4 = [414, -1, 156, -47, 0, 0, 0, 0, 0, -14, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, -6, -9, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sam5 = [389, -12, -153, -27, 1, -8, -8, -5, 15, 19, 5, 5, 1, -6, 0, 7, 0, 0, 4, -10, -7,
            -4, -9, 4, 3, -2, 3, 1, -4, 2, -4, -2, 3, 0, 1, 1, 6, -1, 2, 0, -4, 1, 0, 6, 0, 0,
            2, 1, -1, 0, 3, 2, -1, 4, -2, -2, 0, 2, -1, -2, -5, -2, -1, 0]
    sam6 = [-383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383,
            -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383,
            -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, -383, 560, -1,
            -7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0]
    sam7 = [383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383,
            -383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383, 383,
            383, 383, 383, 383, 383, 383, 383, 383, 560, -1, -7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sam8 = [560, -1, -7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sam9 = [-20273, 305, -1, -7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sam10 = [637, 255, -65]
    sam11 = [637, 510, -65]
    sam12 = [637, 0, -65]
    sam13 = [382, 0, -65]
    sam14 = [127, 0, -65]
    sam15 = [-128, 0, -65]
    sam16 = [-127, 0, -65]
    samples = (sam1, sam2, sam3, sam4, sam5, sam6, sam7, sam8, sam9, sam10, sam11, sam12,
               sam13, sam14, sam15, sam16)
    map(test, samples)

#
##
###
####
##### Decompression.py

def Test_DeQuantize():
    print 'Test_DeQuantize()\n'
    Before = [30, 0, -7, -12, -8, -1, 0, 1, 6, -5, -7, -3, 0, -1, 0, 0, 0, -1, 0, -3, -4, -1,
              4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    arr = array([[Before for x in xrange(11)] for x in xrange(11)])
    DQ = DeQuantize(arr,2)
    Qtrx = matrix([[(1 + (x + y + 1)*2) for x in xrange(8)] for y in xrange(8)])
    print 'First, we have the quantized version.\n',Before
    print 'Next, we have the Qtrx Matrix.\n',Qtrx
    print 'And finally, the end result!\n',DQ[9,9]

if __name__ == "__main__":
    #Test_DCT()
    #Test_Quantize()
    #Test_Run_Length()
    Test_Run_Width()
    #Test_DeQuantize()
