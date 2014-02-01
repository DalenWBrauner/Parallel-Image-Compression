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
filename = raw_input('Filename? ')
i = imread(filename)

# Split_RGB()
Colors = Split_RGB(i)

#
##
### Decompressor Emulator

# main()
final_array = array(Colors).swapaxes(0,2)
imsave('new.png',final_array)
