import os

from controllers.main_controller import Controller


class Run:
    def __init__(self):
        self.controller = Controller()

    def start(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        self.controller.start()


if __name__ == "__main__":
    run = Run()
    run.start()
