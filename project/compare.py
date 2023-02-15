import argparse

import imageio.v3 as iio
import numpy as np

from pathlib import Path
from matplotlib import pyplot as plt

from convert import convert_img


def compare(path: Path):
    name = path.name.split(".")[0]
    assert len(name) > 0

    outputs = [
        Path(f"./dest_imgs/{name}.png"),
        Path(f"./dest_imgs/{name}.jpeg"),
        Path(f"./dest_imgs/{name}.webp")
    ]

    if not all(map(lambda p: p.exists(), outputs)):
        convert_img(p)

    src_data = iio.imread(path)
    img_data = map(iio.imread, outputs)

    combined_diffs = []
    fig, axes = plt.subplots(1, len(outputs))
    for i, img  in enumerate(img_data):
        diff = np.power(src_data - img, 2)
        combined_diffs.append(diff[:,:,0] + diff[:,:,1] + diff[:,:,2])

    combined_diffs = np.array(combined_diffs)
    max_diff = np.max(combined_diffs)
    print(combined_diffs.shape, max_diff)

    for i, ax in enumerate(axes.flat):
        plt.subplot(1,len(outputs),i+1)
        im = plt.imshow(combined_diffs[i,:,:], vmin=0, vmax=max_diff)

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Image Quality Comparison",
        description="Create a plot showing the difference in between different image compression algorithms"
    )

    parser.add_argument("src", help="the source image to be analyzed")
    args = parser.parse_args()

    p = Path(args.src)
    if p.exists():
        compare(p)
