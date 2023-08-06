import time

from .ensemble import View

# Main ABC
class Cluster(object):
    def __init__(self) -> None:
        pass

    def execute():
        pass


class KMeans(Cluster):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, view: View):
        print("Executing clustering algorithm")
        time.sleep(3)


class Ward(Cluster):
    def __init__(self) -> None:
        super().__init__()
        pass