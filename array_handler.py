from numpy import array

def arraymap(function,sequence,dtype=None,esize=1):
    """Performs map() operations to all elements in an array of any shape.
    'dtype' sets the dtype of the array returned.
    'esize' sets the size of an "element" in the array, i.e. how large the
    array should be before we stop recursing through its dimensions and
    apply the function."""
    r = len(sequence.shape)
    return array(arraymap_r(r-1,function,sequence,esize),dtype)

def arraymap_r(r,function,sequence,esize):
    new_sequence = []
    
    if r != esize:
        for element in sequence:
            new_sequence.append(arraymap_r(r-1,function,element,esize))
    else:
        for element in sequence:
            new_sequence.append(function(element))
    
    return new_sequence
