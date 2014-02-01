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

# Compressor Emulator
filename = raw_input('Filename? ')
I = imread(filename)
I_Swapped = I.swapaxes(0,2)
R, G, B, Alpha = I_Swapped

# Decompressor Emulator
I_Combined = array([R, G, B])
I_SwappedAgain = I_Combined.swapaxes(0,2)
imsave('new.png',I_SwappedAgain)
