"""
.                                   .
|   Resaver.py                      |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *
"""

from scipy.ndimage import imread
from scipy.misc import imsave
from numpy import array

from Compression import *
from Decompression import *

#
##
### Compressor Emulator

# main()
filename = 'C:\Users\Dalen\Documents\GitHub\Parallel-Image-Compression\Bird.png'
i = imread(filename)

# Split_RGB()
Colors = Split_RGB(i)

# Split_Blocks()
R_Blocks, G_Blocks, B_Blocks = map(Split_Blocks, Colors)

# Calc_DCT()
R_DCTs = arraymap(Calc_DCT, R_Blocks, esize=2)
G_DCTs = arraymap(Calc_DCT, G_Blocks, esize=2)
B_DCTs = arraymap(Calc_DCT, B_Blocks, esize=2)
        

#
##
### Decompressor Emulator

# Undo_DCT()
R_Blocks = arraymap(Undo_DCT, R_DCTs, esize=2)
G_Blocks = arraymap(Undo_DCT, G_DCTs, esize=2)
B_Blocks = arraymap(Undo_DCT, B_DCTs, esize=2)

# Merge_Blocks()
R_Merged, G_Merged, B_Merged = map(Merge_Blocks, (R_Blocks, G_Blocks, B_Blocks))
Colors = R_Merged, G_Merged, B_Merged

# main()
final_array = array(Colors).swapaxes(0,2)
imsave('new.png',final_array)

print "All done!"
