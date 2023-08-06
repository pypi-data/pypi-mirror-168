import base64
import blosc
import numpy as np


def gsNpCompressBase64WithShape(frame):
    bytes_array = frame.tostring()
    zframe = blosc.compress(bytes_array)
    b64frame = base64.b64encode((zframe))
    return b64frame.decode('utf-8'), frame.shape[0], frame.shape[1], frame.shape[2]


def gsNpCompressWithShape(frame):
    bytes_array = frame.tostring()
    zframe = blosc.compress(bytes_array)
    return zframe, frame.shape[0], frame.shape[1], frame.shape[2]


def gsNumpyDecompressBase64(b64frame, w, h, d):
    zframe = base64.b64decode(b64frame.encode('utf-8'))
    frame = np.frombuffer(blosc.decompress(zframe, True), dtype=np.uint8)
    frame.shape = (int(w), int(h), int(d))
    return frame


def gsNumpyDecompress(zframe, w, h, d):
    frame = np.frombuffer(blosc.decompress(zframe, True), dtype=np.uint8)
    frame.shape = (int(w), int(h), int(d))
    return frame


def gsNpToBytesWithShape(frame):
    return frame.tobytes(), frame.shape[0], frame.shape[1], frame.shape[2]


def gsBytesToNPArray(frame):
    nparray = np.frombuffer(frame[0], dtype=np.uint8)
    nparray.shape = (int(frame[1]), int(frame[2]), int(frame[3]))
    return nparray


def handleparametermissing(request, *args):
    for parameter in args:
        if request.get(parameter) is None:
            raise ValueError('Missing paramter: ' + parameter)
