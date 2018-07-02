import numpy as np
import dct
import zigzag

from PIL import Image
from runlength import encode, decode

QR = np.array([
            [16, 11, 10, 16,  24,  40,  51,  61],
            [12, 12, 14, 19,  26,  58,  60,  55],
            [14, 13, 16, 24,  40,  57,  69,  56],
            [14, 17, 22, 29,  51,  87,  80,  62],
            [18, 22, 37, 56,  68, 109, 103,  77],
            [24, 35, 55, 64,  81, 104, 113,  92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103,  99]])

QC = np.array([
            [17, 18, 24, 47, 99, 99, 99, 99],
            [18, 21, 26, 66, 99, 99, 99, 99],
            [24, 26, 56, 99, 99, 99, 99, 99],
            [47, 66, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99]])

T = np.array([
            [ 0.299,  0.587,  0.114],
            [-0.169, -0.334,  0.500],
            [ 0.615, -0.419, -0.081]])

iT = np.linalg.inv(T)


def rgb_to_yuv(rgb_array):
    yuv_array = [[np.ravel(np.matmul(T, np.array([y]).T))
                  for y in x ] for x in rgb_array]
    return np.array(yuv_array)


def yuv_to_rgb(yuv_array):
    rgb_array = [[np.ravel(np.matmul(iT, np.array([y]).T))
                  for y in x ] for x in yuv_array]
    return np.array(rgb_array)


def split_channel(img):
    h = img.shape[0]
    w = img.shape[1]
    r = np.empty([h, w])
    g = np.empty([h, w])
    b = np.empty([h, w])
    for x in range(h):
        for y in range(w):
            r[x][y], g[x][y], b[x][y] = img[x,y]
    return r, g, b


def slice(a, chunk_size=8):
    n = a.shape[0]
    m = a.shape[1]
    c = np.empty((n, m))
    c.fill(0)
    c[:a.shape[0], :a.shape[1]] = a
    c = c.reshape(n // chunk_size, chunk_size, m // chunk_size, chunk_size)
    c = c.transpose(0, 2, 1, 3).reshape(n // chunk_size, m // chunk_size, chunk_size, chunk_size)
    return c

merge = lambda a: a.transpose(0, 2, 1, 3).reshape(-1, a.shape[1] * a.shape[3])

def rdivision(a, b):
    c = np.zeros_like(a);
    [h, w] = a.shape
    for i in range(h):
        for j in range(w):
            c[i][j] = a[i][j] / b[i][j]
    return c

def hadamard(a, b):
    c = np.zeros_like(a);
    [h, w] = a.shape
    for i in range(h):
        for j in range(w):
            c[i][j] = a[i][j] * b[i][j]
    return c

def quantize(img, channel='lum'):
    q = QR if channel is 'lum' else QC
    fq = [[rdivision(y, q) for y in x] for x in img]
    return np.array(np.round(fq, 0), dtype=int)


def dequantize(img, channel):
    q = QR if channel is 'lum' else QC
    f_deq = [[hadamard(y, q) for y in x] for x in img]
    return np.array(f_deq, dtype=int)
