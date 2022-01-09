from pathlib import Path

import cv2
import face_recognition

# from imutils import paths
from pprint import pprint

DETECTION_METHOD = "CNN"
IMAGES_FOLDER = "data"

SUPPORTED_IMAGES_FORMATS = [".jpg", ".jpeg", ".png"]


def main():
    images_paths = []
    for type in SUPPORTED_IMAGES_FORMATS:
        images_paths += list(Path(IMAGES_FOLDER).rglob(f"*{type}"))

    images_paths = images_paths[:10]

    for i, image_path in enumerate(images_paths):
        print("[INFO] processing image {}/{}".format(i + 1, len(images_paths)))
        print(image_path)
        image = cv2.imread(str(image_path))
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb, model=DETECTION_METHOD)
        print(boxes)


if __name__ == "__main__":
    main()
