import numpy as np

def hitung_sudut(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ab = a - b
    cb = c - b

    cosine = np.dot(ab, cb) / (
        np.linalg.norm(ab) *
        np.linalg.norm(cb)
    )

    sudut = np.degrees(
        np.arccos(
            np.clip(cosine, -1.0, 1.0)
        )
    )

    return sudut


def hitung_jarak(p1, p2):

    p1 = np.array(p1)
    p2 = np.array(p2)

    return np.linalg.norm(p1 - p2)