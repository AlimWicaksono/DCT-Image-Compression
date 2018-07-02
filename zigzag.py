import numpy as np
import math
'''
def array(size):
    data = np.zeros(size * size).reshape([size, size])
    i = j = 1
    for element in range(size * size):
        data[i - 1][j - 1] = element
        if (i + j) % 2 is 0:
            if j < size:
                j = j + 1
            else:
                i = i + 2
            if i > 1:
                i = i - 1
        else:
            if i < size:
                i = i + 1
            else:
                j = j + 2
            if j > 1:
                j = j - 1
    return data
'''

def scan(array):
    result = []
    [h, w] = array.shape
    i = j = 1
    for element in range(h * w):
        result.append(array[i - 1][j - 1])
        if (i + j) % 2 is 0:
            if j < h:
                j = j + 1
            else:
                i = i + 2
            if i > 1:
                i = i - 1
        else:
            if i < w:
                i = i + 1
            else:
                j = j + 2
            if j > 1:
                j = j - 1
    return result


def arange(array):
    size = int(math.sqrt(len(array)))
    block = np.zeros(size * size).reshape([size, size])
    i = j = 1
    for element in array:
        block[i - 1][j - 1] = element
        if (i + j) % 2 is 0:
            if j < size:
                j = j + 1
            else:
                i = i + 2
            if i > 1:
                i = i - 1
        else:
            if i < size:
                i = i + 1
            else:
                j = j + 2
            if j > 1:
                j = j - 1
    return block
