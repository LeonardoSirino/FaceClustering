from src.config import IMAGES_FOLDER
from src.encoder import Encoder
from src.storage.controller import Controller
from src.clusterizer import Clusterizer

controller = Controller()


# encoder = Encoder(controller)
# paths = encoder.get_images_paths(IMAGES_FOLDER,
#                                  shuffle=True,
#                                  count=10)
# encoder.encode_images(paths)

clusterizer = Clusterizer(controller)
clusterizer.clusterize(reclusterize=False)
