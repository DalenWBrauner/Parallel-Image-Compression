"""
.                                   .
|   Resaver.py                      |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *
"""
import pickle

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

# Write_To()
final_string = chr(q) + chr(R_RunW.shape[0]) + chr(R_RunW.shape[1])
for arr in R_RunW:
    for code in arr:
        final_string += code
for arr in G_RunW:
    for code in arr:
        final_string += code
for arr in B_RunW:
    for code in arr:
        final_string += code

# Arbitrary Pickling
f = open('delete_me.arbitrary', 'wb')
pickle.dump(final_string, f)
f.close()

# Clearing the final_string data
final_string = ''

#
##
### Decompressor Emulator

# Arbitrary Pickling
f = open('delete_me.arbitrary', 'rb')
final_string = pickle.load(f)
f.close()

# Decompress()
quality = ord(final_string[0])

# Unpack_Blocks()
R, G, B = Unpack_Blocks(final_string[1:])

# DeQuantize()
R_DQ = DeQuantize(R,q)
G_DQ = DeQuantize(G,q)
B_DQ = DeQuantize(B,q)

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
