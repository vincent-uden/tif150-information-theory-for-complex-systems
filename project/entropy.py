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
#
# How does the fact that the image is finite affect the entropy results???
#   For the random image, it's block entropy should always be 8 bits per symbol
#   if it was infinite. It deviates from this at 3 bytes block length, since
#   there are less combinations availible for storage in the image than there
#   are possible 3-byte combinations: (512*512*3=786432, 256*256*256=16777216)

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

    return np.sum( p * np.log2(1.0/p) )

def S_m_bytes(data: np.ndarray, m: int) -> float:
    total = 0
    patterns = defaultdict(lambda: 0)
    for i in range(len(data)-m):
        seq = data[i:i+m]
        patterns[tuple(seq)] += 1
        total += 1

    entropy = 0
    for v in patterns.values():
        p = v / float(total)
        entropy += p * np.log2(1.0/p)

    return entropy

def load_raw_file(path: Path):
    r_bytes = np.fromfile(str(path) + ".red", dtype="uint8")
    g_bytes = np.fromfile(str(path) + ".grn", dtype="uint8")
    b_bytes = np.fromfile(str(path) + ".blu", dtype="uint8")

    combined = np.zeros((r_bytes.shape[0]*3), dtype="uint8")
    for i, (r,g,b) in enumerate(zip(r_bytes,g_bytes,b_bytes)):
        combined[i*3] = r
        combined[i*3+1] = g
        combined[i*3+2] = b

    return combined


def file_entropy(path: Path):
    return

if __name__ == "__main__":
    paths = [
        Path("./dest_imgs/baboon.raw"),
        Path("./dest_imgs/baboon.png"),
        Path("./dest_imgs/baboon.jpeg"),
        Path("./dest_imgs/baboon.webp"),
        Path("./src_imgs/baboon.tiff"),
    ]
    for p in paths:
        print(p)
        if p.suffix == ".raw":
            data = load_raw_file(p)
        else:
            data = np.fromfile(p, dtype="uint8")

        M = 30
        entropies = np.zeros(M)
        for m in trange(1,M+1):
            entropies[m-1] = S_m_bytes(data, m) / m

        print(entropies)

        np.save(f"./entropy_results/{p.name}.npy", entropies)
