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
filename = 'C:\Users\Dalen\Documents\GitHub\Parallel-Image-Compression\Winter.png'
q = 11
i = imread(filename)

# Split_RGB()
Colors = Split_RGB(i)

# Split_Blocks()
R_Blocks, G_Blocks, B_Blocks = map(Split_Blocks, Colors)

# Calc_DCT()
R_DCTs = arraymap(Calc_DCT, R_Blocks, esize=2)
G_DCTs = arraymap(Calc_DCT, G_Blocks, esize=2)
B_DCTs = arraymap(Calc_DCT, B_Blocks, esize=2)

# Quantize()
R_Q = Quantize(R_DCTs,q)
G_Q = Quantize(G_DCTs,q)
B_Q = Quantize(B_DCTs,q)

# Run_Width()
R_RunW = arraymap(Run_Width, R_Q)
G_RunW = arraymap(Run_Width, G_Q)
B_RunW = arraymap(Run_Width, B_Q)

#
##
### Decompressor Emulator

# Decode_Width()
##R_DeW = arraymap(Decode_Width, R_RunW)
##G_DeW = arraymap(Decode_Width, G_RunW)
##B_DeW = arraymap(Decode_Width, B_RunW)
# Create lists
R_DeW = [[] for x in xrange(R_RunW.shape[0])]
G_DeW = [[] for x in xrange(G_RunW.shape[0])]
B_DeW = [[] for x in xrange(B_RunW.shape[0])]
# Loop through array, decode+append to list
r = -1
for arr in R_RunW:
    r += 1
    for code in arr:
         R_DeW[r].append(Decode_Width(code))

g = -1
for arr in G_RunW:
    g += 1
    for code in arr:
         G_DeW[g].append(Decode_Width(code))

b = -1
for arr in B_RunW:
    b += 1
    for code in arr:
         B_DeW[b].append(Decode_Width(code))
# Convert to array
R_DeW, G_DeW, B_DeW = array(R_DeW), array(G_DeW), array(B_DeW)

# DeQuantize()
R_DQ = DeQuantize(R_DeW,q)
G_DQ = DeQuantize(G_DeW,q)
B_DQ = DeQuantize(B_DeW,q)

# Undo_DCT()
R_Blocks = arraymap(Undo_DCT, R_DQ, esize=2)
G_Blocks = arraymap(Undo_DCT, G_DQ, esize=2)
B_Blocks = arraymap(Undo_DCT, B_DQ, esize=2)

# Merge_Blocks()
R_Merged, G_Merged, B_Merged = map(Merge_Blocks, (R_Blocks, G_Blocks, B_Blocks))
Colors = R_Merged, G_Merged, B_Merged

# main()
final_array = array(Colors).swapaxes(0,2)
imsave('new.png',final_array)

print "All done!"
