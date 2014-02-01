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

### Calc_DCT()
##R_DCTs = arraymap(Calc_DCT, R_Blocks, dtype=int, esize=2)
##G_DCTs = arraymap(Calc_DCT, G_Blocks, dtype=int, esize=2)
##B_DCTs = arraymap(Calc_DCT, B_Blocks, dtype=int, esize=2)

## Calc_DCT() sans arraymap()
##NewR = []
##NewG = []
##NewB = []
##for x in xrange(R_Blocks.shape[0]):
##    NewR.append([])
##    NewG.append([])
##    NewB.append([])
##    for y in xrange(R_Blocks.shape[1]):
##        NewR[x].append(Calc_DCT(R_Blocks[x,y]))
##        NewG[x].append(Calc_DCT(G_Blocks[x,y]))
##        NewB[x].append(Calc_DCT(B_Blocks[x,y]))
##R_DCTs = array(NewR, dtype=int)
##G_DCTs = array(NewG, dtype=int)
##B_DCTs = array(NewB, dtype=int)
        

#
##
### Decompressor Emulator

### Undo_DCT()
##Just_R = arraymap(Undo_DCT, R_DCTs, dtype=int, esize=2)
##Just_G = arraymap(Undo_DCT, G_DCTs, dtype=int, esize=2)
##Just_B = arraymap(Undo_DCT, B_DCTs, dtype=int, esize=2)

## Undo_DCT() sans arraymap()
##NewR = []
##NewG = []
##NewB = []
##for x in xrange(R_Blocks.shape[0]):
##    NewR.append([])
##    NewG.append([])
##    NewB.append([])
##    for y in xrange(R_Blocks.shape[1]):
##        NewR[x].append(Undo_DCT(R_DCTs[x,y]))
##        NewG[x].append(Undo_DCT(G_DCTs[x,y]))
##        NewB[x].append(Undo_DCT(B_DCTs[x,y]))
##Just_R = array(NewR, dtype=int)
##Just_G = array(NewG, dtype=int)
##Just_B = array(NewB, dtype=int)
Just_R, Just_G, Just_B = R_Blocks, G_Blocks, B_Blocks

# Merge_Blocks()
R_Merged, G_Merged, B_Merged = map(Merge_Blocks, (Just_R, Just_G, Just_B))
Colors = R_Merged, G_Merged, B_Merged

# main()
final_array = array(Colors).swapaxes(0,2)
imsave('new.png',final_array)

print "All done!"
