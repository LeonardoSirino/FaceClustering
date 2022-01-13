import logging

from src.clusterizer import Clusterizer
from src.config import IMAGES_FOLDER
from src.encoder import Encoder
from src.storage.controller import Controller

logging.basicConfig(level=logging.INFO)

controller = Controller()

encoder = Encoder(controller)
paths = encoder.get_images_paths(IMAGES_FOLDER,
                                 shuffle=True,
                                 count=2000)
encoder.encode_images(paths)

clusterizer = Clusterizer(controller)
clusterizer.clusterize(reclusterize=True)
