import numpy as np

from matplotlib import pyplot as plt

if __name__ == "__main__":
    name = "random"

    png  = np.load(f"entropy_results/{name}.png.npy")
    jpeg = np.load(f"entropy_results/{name}.jpeg.npy")
    webp = np.load(f"entropy_results/{name}.webp.npy")
    tiff = np.load(f"entropy_results/{name}.tiff.npy")
    raw  = np.load(f"entropy_results/{name}.raw.npy")

    x = np.arange(png.shape[0]) + 1
    plt.plot(x, png, label="PNG")
    plt.plot(x, jpeg, label="JPEG")
    plt.plot(x, webp, label="WEBP")
    plt.plot(x, tiff, label="TIFF")
    plt.plot(x, raw, label="RAW")
    plt.title(name)
    plt.xlabel("Block size ($m$)")
    plt.ylabel("Block entropy per symbol ($S_m/m$)")
    plt.legend()
    plt.grid()
    plt.savefig(f"./plots/{name}.pdf")
    plt.show()
