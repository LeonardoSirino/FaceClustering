from .storage.controller import Controller, Labels, Location
from sklearn.cluster import DBSCAN
import numpy as np


class Clusterizer:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    def clusterize(self, reclusterize=False) -> None:
        """Clusterize all images in the database

        Arguments:
            reclusterize {bool} -- if set to true, the current label is discarded (default: {False})
        """
        locations = self.controller.get_locations(not reclusterize)
        encodings = [np.frombuffer(location.encoding)
                     for location in locations]

        clt = DBSCAN(metric='euclidean', n_jobs=-1)
        clt.fit(encodings)

        unique_labels = np.unique(clt.labels_)
        labels = [Labels(id_=int(label))
                  for label in unique_labels if label != -1]

        max_id = 0
        if not reclusterize:
            label_ids = self.controller.get_label_ids()

            if label_ids:
                max_id = max(label_ids) + 1

            for label in labels:
                label.id_ += max_id

        else:
            self.controller.drop_labels()

        self.controller.add_labels(labels)

        for loc, label in zip(locations, clt.labels_):
            if label != -1:
                loc.label_id = label + max_id

        locations = [loc for loc in locations if loc.label_id is not None]
        self.controller.update_locations(locations)

    def export_images_clusters(self):
        # TODO maybe this method should be in a different file
        """Creates a folder for each table and populates it with pictures segments"""
