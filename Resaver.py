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

#
##
### Decompressor Emulator

# Merge_Blocks()
R_Merged, G_Merged, B_Merged = map(Merge_Blocks, (R_Blocks, G_Blocks, B_Blocks))
Colors = R_Merged, G_Merged, B_Merged

# main()
final_array = array(Colors).swapaxes(0,2)
imsave('new.png',final_array)

print "All done!"
