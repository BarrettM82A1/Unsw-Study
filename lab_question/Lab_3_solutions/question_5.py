# Written by Eric Martin for COMP9021


'''
Performs operations on encodings of a set of (distinct)
nonnegative integers {n_1, ..., n_k} as 2^{n_1} + ... + 2^{n_k}.
'''


def display_encoded_set(encoded_set):
    '''
    Displays the members of the set encoded by the argument,
    from smallest to largest element, in increasing order.
    
    >>> display_encoded_set(0)
    {}
    >>> display_encoded_set(1)
    {0}
    >>> display_encoded_set(3)
    {0, 1}
    >>> display_encoded_set(76)
    {2, 3, 6}
    '''
    print('{', end = '')
    i = 0
    if encoded_set:
        while encoded_set % 2 == 0:
            encoded_set //= 2
            i += 1
        print(i, end = '')
        encoded_set //= 2
        i += 1
    while encoded_set:
        if encoded_set % 2:
            print(',', i, end = '')
        encoded_set //= 2
        i += 1
    print('}')

def set_encoding(set_of_nonnegative_integers):
    '''
    Encodes a set and returns the encoding.
    Here an empty set of curly braces provided as argument
    denotes the empty set, not the empty dictionary.
    
    >>> set_encoding({})
    0
    >>> set_encoding({0})
    1
    >>> set_encoding({0, 1})
    3
    >>> set_encoding({2, 3, 6})
    76
    '''
    encoding = 0
    while set_of_nonnegative_integers:
        encoding += 1 << set_of_nonnegative_integers.pop()
    return encoding

def is_in_encoded_set(nonnegative_integer, encoded_set):
    '''
    Returns True or False depending on whether the first argument
    belongs to the set encoded as the second argument.
    
    >>> is_in_encoded_set(0, 0)
    False
    >>> is_in_encoded_set(0, 1)
    True
    >>> is_in_encoded_set(3, 76)
    True
    >>> is_in_encoded_set(4, 76)
    False
    '''
    return 1 << nonnegative_integer & encoded_set != 0

def cardinality(encoded_set):
    '''
    Returns the number of elements in the set
    encoding as the argument.
    
    >>> cardinality(0)
    0
    >>> cardinality(1)
    1
    >>> cardinality(76)
    3
    '''
    nb_of_elements = 0
    while encoded_set:
        if encoded_set % 2:
            nb_of_elements += 1
        encoded_set //= 2
    return nb_of_elements


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
