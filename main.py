import os

from chess_tui.controllers.main_ctl import Controller


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.mkdir("data")
    controllers = Controller()
    controllers.start()
