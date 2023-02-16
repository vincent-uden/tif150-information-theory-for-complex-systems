import numpy as np

from collections import defaultdict
from pathlib import Path

from tqdm import trange


# One angle would be to consider only the image data for the entropy
# calculation. Different formats contain differing amounts of redundant
# information. This does pose a problem though. Lots of information could be
# front-loaded in the header information using inefficent encoding schemes
# which would distort the results.
#
# Therefore this file does an entropy calculation over the entire binary data
# of the image.

def binary_data(path: Path) -> np.ndarray:
    f_bytes = np.fromfile(path, dtype="uint8")
    return np.unpackbits(f_bytes)

def bits_to_int(bits: np.ndarray) -> int:
    L = bits.shape[0]
    a = 2**np.arange(L)[::-1]
    return bits @ a

def S_m(data: np.ndarray, m: int) -> float:

    count = np.zeros((2**m))
    for i in range(data.shape[0]-m):
        seq = data[i:i+m]
        count[bits_to_int(seq)] += 1

    total = np.sum(count)
    p = count / total
    print(total)

    return np.sum( p * np.log2(1.0/p) )

def S_m_bytes(data: np.ndarray, m: int) -> float:

    total = 0
    patterns = defaultdict(lambda: 0)
    for i in range(len(data)-m):
        seq = data[i:i+m]
        patterns[seq] += 1
        total += 1

    entropy = 0
    for v in patterns.values():
        p = v / float(total)
        entropy += p * np.log2(1.0/p)

    return entropy


def file_entropy(path: Path):
    return

if __name__ == "__main__":
    png_path = Path("./dest_imgs/baboon.png")

    data = np.fromfile(png_path, dtype="uint8")
    char_seq = str([ chr(i) for i in data ])

    M = 30
    entropies = np.zeros(M)
    for m in trange(1,M+1):
        entropies[m-1] = S_m_bytes(char_seq, m) / m

    print(entropies)

    np.save("output", entropies)
