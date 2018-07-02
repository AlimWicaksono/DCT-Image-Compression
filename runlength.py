import numpy as np

def encode(data, dtype):
    j = i = 0
    data = np.array(data, dtype=dtype)
    stream = data.ravel(order='C')
    l = len(stream)
    [c, h, w, b] = data.shape
    encoded = [[c, h], [w, b]]
    while i < l:
        value = stream[i]
        rlen = 1
        while i + 1 < l and rlen & 0xff < 255 and stream[i] == stream[i + 1]:
            rlen = rlen + 1
            i = i + 1
        encoded.append([value, rlen])
        i = i + 1
    return np.array(encoded, dtype=dtype)


def decode(encoded_stream):
    [c, h] = encoded_stream[0]
    [w, b] = encoded_stream[1]
    decoded = []
    for data in encoded_stream[2:]:
        decoded.extend([data[0] for i in range(data[1] & 0xff)])
    return np.array(decoded).reshape([c, h, w, b])
