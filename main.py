import os

from controllers.main_controller import Controller


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.mkdir("data")
    ctl = Controller()
    ctl.main_run()
