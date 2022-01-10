import pickle
from pathlib import Path

import cv2
import face_recognition
from tqdm import tqdm

from .config import (
    SUPPORTED_IMAGES_FORMATS,
    IMAGES_FOLDER,
    DETECTION_METHOD,
    OUTPUT_FILE,
)


def main():
    images_paths = []
    for type in SUPPORTED_IMAGES_FORMATS:
        images_paths += list(Path(IMAGES_FOLDER).rglob(f"*{type}"))

    # images_paths = images_paths[:10]
    data = []
    for image_path in tqdm(images_paths):
        image = cv2.imread(str(image_path))
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb, model=DETECTION_METHOD)

        encodings = face_recognition.face_encodings(rgb, boxes)
        d = [
            {"imagePath": image_path, "loc": box, "encoding": enc}
            for (box, enc) in zip(boxes, encodings)
        ]
        data.extend(d)

    f = open(OUTPUT_FILE, "wb")
    f.write(pickle.dumps(data))
    f.close()


if __name__ == "__main__":
    main()
