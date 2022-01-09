from pathlib import Path

# import cv2
# import face_recognition
# from imutils import paths
from pprint import pprint

DETECTION_METHOD = "CNN"
IMAGES_FOLDER = "data"

SUPPORTED_IMAGES_FORMATS = [".jpg", ".jpeg", ".png"]


def main():
    images_paths = []
    for type in SUPPORTED_IMAGES_FORMATS:
        images_paths += list(Path(IMAGES_FOLDER).rglob(f"*{type}"))

    pprint(images_paths)

    # for (i, imagePath) in enumerate(imagePaths):
    #     print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    #     print(imagePath)
    #     image = cv2.imread(imagePath)
    #     rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #     boxes = face_recognition.face_locations(rgb, model=args["detection_method"])


if __name__ == "__main__":
    main()