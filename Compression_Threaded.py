"""
.                                   .
|   Compression_Threaded.py         |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *

"""
# Builtin libs
import math, time, random
from math import sqrt, cos, pi
from threading import Thread, Lock

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
    print "Win:"
    print "winter-wallpaper-24.png"
    print "bird.png"
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
    The majority of this should be parallelized.
    'i' Should be a Length*Width*4 array of RGB color values.
    'q' Should be the user-requested quality of the image."""

    # Split the colors
    colors = list(Split_RGB(i))

    # Calculate the number of 8x8 blocks to-be and start a quota
    hh = colors[0].shape[0]/8
    ww = colors[0].shape[1]/8
    quota = Quota(hh*ww*3)
    
    # Create a BlockThread for each 8x8 block in each color.
    try:
        for w in xrange(3):
            for y in xrange(ww):
                for x in xrange(hh):
                    BlockThread(colors, w, x, y, q, quota).start()
    finally:
        e = "\n\n\nAccomplished:\n\n\n"
        e += "w: "+str(w)+" out of 3.\n"
        e += "y: "+str(y)+" out of "+str(ww)+".\n"
        e += "x: "+str(x)+" out of "+str(hh)+".\n"
        print e

#
##
### Thread objects:
class BlockThread(Thread):

    def __init__(self, colors, w, x, y, quality, quota):
        """A thread to be run for each 8x8 block in an image.
        'colors' = The almighty container for everything.
        'w' = Which array in 'colors' data is copied to.
        'x' = The x position of the 8x8 in the array.
        'y' = The y position of the 8x8 in the array.
        'quality' = The user-requested quality value.
        'quota' = The Quota for reporting to when finished."""
        Thread.__init__(self, name=str((w, x, y)))
        self.block = colors[w][(x*8) : (x*8+8), (y*8) : (y*8+8)]
        self.colors = colors
        self.w, self.x, self.y, self.q = w, x, y, quality
        self.quota = quota

    def run(self):
        """Threads currently sleep from somewhere between 0-10 seconds, then claim to be done."""
        time.sleep(random.randint(0,10))
        # Time to tell everyone we're finished!
        self.quota.lock.acquire()
        try:
            self.quota.all_done(self.w,self.x,self.y)
        finally:
            self.quota.lock.release()
            # Huzzah! Welcome to the party of finished threads!
        

##    def run(self):
##        
##        t0 = time.clock()
##        Blocks = Split_Blocks(self.colordata)
##        t1 = time.clock()
##        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to Split Blocks.\n"
##        print msg
##        
##        t0 = time.clock()
##        DCT = arraymap(Calc_DCT, Blocks, dtype=int, esize=2)
##        t1 = time.clock()
##        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to calculate DCTs.\n"
##        print msg
##        
##        t0 = time.clock()
##        Q = Quantize(DCT, self.q)
##        t1 = time.clock()
##        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to Quantize.\n"
##        print msg
##        
##        t0 = time.clock()
##        RunLen = arraymap(Run_Length, Q)
##        t1 = time.clock()
##        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to apply RLE algorithms.\n"
##        print msg
##        
##        t0 = time.clock()
##        Final = Huffman(RunLen)
##        t1 = time.clock()
##        msg = str(self.name)+" took "+str(round(t1-t0,6))+" seconds to run Huffman Codes.\n"
##        print msg
##        
##        # The final line of this function should be:
##        self.finished[self.spot] = True

#
##
### A Wild object Appeared!
class Quota(object):
        def __init__(self,limit):
            self.lock = Lock()
            self.guest_list = []
            self._quota = limit

        def all_done(self,w,x,y):
            """A function to be called when a BlockThread has finished.
            The idea is that this function checks if the other threads have finished yet.
            If they have, it then runs the final stretch of the program.
            Otherwise, nothing happens.
            Some error checking is thrown in, just in case something bizzare happens."""
            # Debugging
            s = "Out of "+str(self._quota)+", Arrived Guests: "+str(len(self.guest_list))
            print s

            # Check to assure the guest has not already arrived
            if str((w,x,y)) in self.guest_list:
                # This will hopefully never pass
                reason = "Somehow, ("+str(w)+', '+str(x)+', '+str(y)+") arrived to the party twice."
                raise IndexError(reason)
            
            # Add the guest to the guest list
            self.guest_list.append(str((w,x,y)))

            # Check to assure the quota has not been exceeded
            if len(self.guest_list) > self._quota:
                reason = "Somehow, the guest_list has exceeded the quota..."
                raise IndexError(reason)
            
            elif len(self.guest_list) == self._quota:
                # I wasn't kidding when I said it runs the final stretch.
                final_stretch()

def final_stretch():
    print "Show's over, everyone!"
    print "We can all go home!"


if __name__ == "__main__":
    main()
    IDLE_safety_hazard()
