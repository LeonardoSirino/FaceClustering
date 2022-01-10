import cv2
import numpy as np


def read_image(image_path: str) -> np.ndarray:
    stream = open(image_path, "rb")
    bytes = bytearray(stream.read())
    array = np.asarray(bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_UNCHANGED)

    return image
