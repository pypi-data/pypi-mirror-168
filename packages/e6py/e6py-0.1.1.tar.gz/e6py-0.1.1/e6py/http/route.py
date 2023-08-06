class Route:
    def __init__(self, method: str, path: str):
        self.path: str = path
        self.method: str = method
        self.url: str = "{path}".format(path=self.path)


class RawRoute(Route):
    def __init__(self, method: str, path: str):
        self.path: str = path
        self.method: str = method
        self.url = self.path
