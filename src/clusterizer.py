from .storage.controller import Controller, Labels, Location


class Clusterizer:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    def clusterize(self, reclusterize=False) -> None:
        locations = self.controller.get_locations(not reclusterize)
        print(locations)
