"""
.                                   .
|   Run_Me.py                       |
|   Written by Dalen W. Brauner     |
|   Status: Unfinished              |
*                                   *
"""
# Builtin libs
import pickle

# Required libs
from scipy.ndimage import imread
from scipy.misc import imsave
from numpy import array

# Custom Libs
import Compression
import Decompression

def main():
    """ User Interface """
    
    # Ask the user which function they wish to call
    CALL = {"1":Compression,"2":Decompression,"3":Both}
    print "Please enter one of the following integers to make your selection:"
    print "1: Compression"
    print "2: Decompression"
    print "3: Both"
    func = raw_input('')
    while func not in CALL:
        print "Sorry; please enter 1, 2 or 3 to indicate your response."
        func = raw_input('')
    
    # Ask the user whether they'd like to see timings
    YE = ['y','yes']
    NO = ['n','no']
    print "Would you like to time it? (Y/N)"
    timepref = raw_input('')
    while (timepref.lower() not in YE) and (timepref.lower() not in NO):
        print "Sorry; please enter y, n, yes or no to indicate your response."
        timepref = raw_input('')
    
    # Ask the user for the location of their file
    print "Could you please give me the file location in full? "
    filename = raw_input('')
    
    # Call their desired function
    CALL[func](timepref.lower() in YE, filename)

def Compression(timepref, filename):
    """ Image Compressor """
    
    # Ask the user for the quality of the image
    print "Lastly: What level of compression would you prefer?"
    print "(Enter any positive, nonzero integer.)"
    print "(Smaller numbers yield higher picture quality.)"
    print "(Larger numbers yield higher compression rates.)"
    quality = input('')
    while type(quality) != int or quality < 1:
        "Sorry; please enter an integer 1 or greater."
        quality = input('')

    # Error Checking
    if (i.shape[0] %8 != 0) or (i.shape[1] %8 != 0):
        err = "Sorry, Compression() requires an image's dimensions to each be a multiple of 8."
        raise TypeError(err)
    elif (i.shape[0] > 2040) or (i.shape[1] > 2040):
        err = "Sorry, Compression() requires an image's dimensions to each be smaller than 2040."
        raise TypeError(err)
    
    raise NotImplementedError

def Decompression(timepref, filename):
    """ Image Decompressor """

    raise NotImplementedError

def Both(timepref, filename):
    """ Automatically Compresses and Decompresses a file """

    raise NotImplementedError
