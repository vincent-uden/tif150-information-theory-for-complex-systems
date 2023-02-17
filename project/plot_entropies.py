import numpy as np
import os

from matplotlib import pyplot as plt
from pathlib import Path

def plot(name: str):
    png  = np.load(f"entropy_results/{name}.png.npy")
    jpeg = np.load(f"entropy_results/{name}.jpeg.npy")
    webp = np.load(f"entropy_results/{name}.webp.npy")
    tiff_lzw = np.load(f"entropy_results/{name}_lzw.tiff.npy")
    tiff = np.load(f"entropy_results/{name}.tiff.npy")

    x = np.arange(png.shape[0]) + 1
    plt.plot(x, png, label="PNG")
    plt.plot(x, jpeg, label="JPEG")
    plt.plot(x, webp, label="WEBP")
    plt.plot(x, tiff_lzw, label="TIFF (LZW)")
    plt.plot(x, tiff, label="TIFF (RAW)")
    plt.title(name)
    plt.xlabel("Block size ($m$)")
    plt.ylabel("Block entropy per symbol ($S_m/m$)")
    plt.ylim((0,8))
    plt.legend()
    plt.grid()
    plt.savefig(f"./plots/{name}.pdf")

    plt.clf()

def plot_size_mult(name: str):
    png  = np.load(f"entropy_results/{name}.png.npy")
    jpeg = np.load(f"entropy_results/{name}.jpeg.npy")
    webp = np.load(f"entropy_results/{name}.webp.npy")
    tiff_lzw = np.load(f"entropy_results/{name}_lzw.tiff.npy")
    tiff = np.load(f"entropy_results/{name}.tiff.npy")

    paths = [
        Path(f"./dest_imgs/{n}.png"),
        Path(f"./dest_imgs/{n}.jpeg"),
        Path(f"./dest_imgs/{n}.webp"),
        Path(f"./dest_imgs/{n}_lzw.tiff"),
        Path(f"./src_imgs/{n}.tiff")
    ]

    sizes = list(map(os.path.getsize, paths))
    print(sizes)

    x = np.arange(png.shape[0]) + 1
    plt.plot(x, png * sizes[0],      label=f"PNG {sizes[0]/1000:.2f} kb")
    plt.plot(x, jpeg * sizes[1],     label=f"JPEG {sizes[1]/1000:.2f} kb")
    plt.plot(x, webp * sizes[2],     label=f"WEBP {sizes[2]/1000:.2f} kb")
    plt.plot(x, tiff_lzw * sizes[3], label=f"TIFF (LZW) {sizes[3]/1000:.2f} kb")
    plt.plot(x, tiff * sizes[4],     label=f"TIFF (RAW) {sizes[4]/1000:.2f} kb")
    plt.title(name)
    plt.xlabel("Block size ($m$)")
    plt.ylabel("Approximate total entropy")
    plt.ylim((0,8e6))
    plt.legend()
    plt.grid()
    plt.savefig(f"./plots/{name}.pdf")

    plt.clf()

if __name__ == "__main__":
    names = [
        "baboon",
        "peppers",
        "random",
        "white",
    ]

    for n in names:
        plot(n)
