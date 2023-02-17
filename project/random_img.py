import numpy as np

import imageio.v3 as iio

if __name__ == "__main__":
    img_data = np.random.randint(0,256,(512,512,3),dtype="uint8")

    iio.imwrite("src_imgs/random.tiff", img_data)
