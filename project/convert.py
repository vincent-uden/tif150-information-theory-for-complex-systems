#!/usr/bin/env python

# images from the University of Souther California Image Database
# https://sipi.usc.edu/database/database.php

import argparse

import imageio.v3 as iio
import numpy as np

from pathlib import Path

def convert_img(path: Path):
    src = iio.imread(path)
    print(src.shape)

    name = path.name.split(".")[0]
    assert len(name) > 0

    iio.imwrite(f"./dest_imgs/{name}.png", src)
    iio.imwrite(f"./dest_imgs/{name}.jpeg", src, quality=90)
    iio.imwrite(f"./dest_imgs/{name}.webp", src, quality=90)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Image Converter",
        description="Converts a png image to jpg, WebP and AVIF"
    )

    parser.add_argument("src", help="the source image to be converted")
    args = parser.parse_args()

    p = Path(args.src)
    if p.exists():
        convert_img(p)
