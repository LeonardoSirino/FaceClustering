
import hashlib
import logging
from pathlib import Path
from typing import List

import cv2
import face_recognition
import pandas as pd
from tqdm import tqdm

from .config import DETECTION_METHOD, SUPPORTED_IMAGES_FORMATS
from .storage.controller import Controller, Image, Location
from .utils import read_image


class Encoder:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    @staticmethod
    def get_images_paths(folder: str,
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

    @staticmethod
    def get_images_hashes(images_paths: List[Path]) -> List[str]:
        hashes = []
        for image_path in images_paths:
            image = read_image(str(image_path))
            hashes.append(hashlib.sha1(image.tobytes()).hexdigest())

        return hashes

    def encode_images(self, images_paths: List[Path]):
        """Detect faces in images and exports its encodings

        Args:
            images_paths (List[Path]): list of paths to images to be encoded
        """
        current_hashes = self.controller.get_images_hashes()

        df = pd.DataFrame(columns=['hash', 'path'])

        df['path'] = images_paths
        df['hash'] = self.get_images_hashes(images_paths)
        df.drop_duplicates(subset='hash', inplace=True)

        new_images = df[~df['hash'].isin(current_hashes)]
        for _, row in tqdm(new_images.iterrows(), total=len(new_images)):
            image = read_image(row['path'])
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(
                rgb, model=DETECTION_METHOD)

            encodings = face_recognition.face_encodings(rgb, boxes)
            locations = []
            for (box, enc) in zip(boxes, encodings):
                location = Location(image_hash=row['hash'],
                                    box=','.join(map(str, box)),
                                    encoding=enc.tobytes())
                locations.append(location)

            image = Image(hash=row['hash'], path=row['path'])

            self.controller.add_images([image])
            self.controller.add_locations(locations)
