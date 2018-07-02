import numpy as np
import math

def transform(array):
    [h, w] = array.shape
    result = np.zeros_like(array, dtype='float')
    for i in range(h):
        for j in range(w):
            ci = 1 / math.sqrt(2)  if i is 0 else 1
            cj =  1 / math.sqrt(2) if j is 0 else 1
            sum = 0
            for k in range(h):
                for l in range(w):
                    dct = array[k][l] * math.cos((2 * k + 1) * i * math.pi / (2 * h))\
                                      * math.cos((2 * l + 1) * j * math.pi / (2 * w))
                    sum = sum + dct
            result[i][j] = 2 * ci * cj * sum / math.sqrt(h * w)
    return result


def inverse(array):
    [h, w] = array.shape
    result = np.zeros(h * w, dtype='float').reshape([h, w])
    for i in range(h):
        for j in range(w):
            sum = 0
            for k in range(h):
                for l in range(w):
                    ci = 1 / math.sqrt(2)  if k is 0 else 1
                    cj =  1 / math.sqrt(2) if l is 0 else 1
                    dct = array[k][l] * ci * cj\
                                      * math.cos((2 * i + 1) * k * math.pi / (2 * h))\
                                      * math.cos((2 * j + 1) * l * math.pi / (2 * w))
                    sum = sum + dct
            result[i][j] = 2 * sum / math.sqrt(h * w)
    return result
