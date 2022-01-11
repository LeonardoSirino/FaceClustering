from src.config import IMAGES_FOLDER
from src.encoder import Encoder

encoder = Encoder()

paths = encoder.get_images_paths(IMAGES_FOLDER,
                                 shuffle=True,
                                 count=15)
encoder.encode_images(paths)
