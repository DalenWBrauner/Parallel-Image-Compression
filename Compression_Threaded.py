"""
.                                   .
|   Compression_Threaded.py         |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *

"""
# Builtin libs
import math, time
from math import sqrt, cos, pi
from threading import Thread

# Required libs
from numpy import matrix, array
from scipy import ndimage as image

# Custom libs
from array_handler import arraymap
from Compression import Split_RGB, Split_Blocks, Calc_DCT, Quantize, Run_Length, Huffman

#
##
### Core functions:
def IDLE_safety_hazard():
    """If a user is running python code from the command line, the command line window is
    more than likely to close before the user has finished reading all output.
    A call to this function after a call to the main function (or at the very end of the
    main function) will ensure non_IDLE windows receieve a prompt to close their window."""
    import sys
    if 'idlelib.run' not in sys.modules:
        raw_input('\n\nPress Enter to Quit.\n')

def main():
    print "What is the filename?"
    print "Hints:"
    print "C:\Users\Dalen\Desktop\winter-wallpaper-24.png"
    print "C:\Users\Dalen\Desktop\\bird.png"
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
    
    F = [False, False, False]
    Colors = list(Split_RGB(i))
    ColorThread('R',Colors,F,0,q).start()
    ColorThread('G',Colors,F,1,q).start()
    ColorThread('B',Colors,F,2,q).start()
    while (False in F):
        pass
    print "\nOkay, the threads have been run! Let's see what's in the basket..."+str(Colors)

#
##
### Thread objects:
class ColorThread(Thread):

    def __init__(self, name, basket, finished, spot, quality):
        """A thread to be run for each color in an image.
        'name' = The name of the thread.
        'basket' = What file object the results are to be inserted into.
        'finished' = A file object for confirming the thread has finished.
        'spot' = The location of insertion into both aforementioned objects.
        'quality' = The level of picture quality the user wishes preserved."""
        Thread.__init__(self, name = name)
        self.name = name
        self.basket = basket
        self.finished = finished
        self.spot = spot
        self.colordata = basket[spot]
        self.q = quality

    def run(self):
        t0 = time.clock()
        Blocks = Split_Blocks(self.colordata)
        t1 = time.clock()
        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to Split Blocks.\n"
        print msg
        
        t0 = time.clock()
        DCT = arraymap(Calc_DCT, Blocks, dtype=int, esize=2)
        t1 = time.clock()
        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to calculate DCTs.\n"
        print msg
        
        t0 = time.clock()
        Q = Quantize(DCT, self.q)
        t1 = time.clock()
        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to Quantize.\n"
        print msg
        
        t0 = time.clock()
        RunLen = arraymap(Run_Length, Q)
        t1 = time.clock()
        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to apply RLE algorithms.\n"
        print msg
        
        t0 = time.clock()
        Final = Huffman(RunLen)
        t1 = time.clock()
        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to run Huffman Codes.\n"
        print msg
        
        # The final line of this function should be:
        self.finished[self.spot] = True

if __name__ == "__main__":
    main()
    IDLE_safety_hazard()
