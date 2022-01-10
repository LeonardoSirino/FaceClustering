import pickle
from pathlib import Path
from typing import List

import cv2
import face_recognition
import numpy as np
from tqdm import tqdm

from config import (DETECTION_METHOD, IMAGES_COUNT, IMAGES_FOLDER, OUTPUT_FILE,
                    SUPPORTED_IMAGES_FORMATS)
from src.utils import read_image


def get_images_paths(folder: Path,
                     shuffle: bool = False,
                     count: int = -1) -> List[Path]:
    images_paths = []
    for type in SUPPORTED_IMAGES_FORMATS:
        images_paths += list(Path(folder).rglob(f"*{type}"))

    if shuffle:
        import random

        random.shuffle(images_paths)

    if count > 0:
        images_paths = images_paths[:count]

    return images_paths


def get_image_encodings(image_path: Path) -> List[dict]:
    image = read_image(str(image_path))
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model=DETECTION_METHOD)

    encodings = face_recognition.face_encodings(rgb, boxes)
    data = [
        {"image_path": image_path, "loc": box, "encoding": enc}
        for (box, enc) in zip(boxes, encodings)
    ]

    return data


def main():
    images_paths = get_images_paths(IMAGES_FOLDER,
                                    count=IMAGES_COUNT,
                                    shuffle=True)
    data = []
    for image_path in tqdm(images_paths):
        d = get_image_encodings(image_path)
        data.extend(d)

    f = open(OUTPUT_FILE, "wb")
    f.write(pickle.dumps(data))
    f.close()


if __name__ == "__main__":
    main()
