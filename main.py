import os

from views.view_menu import Controller

if not os.path.exists("data"):
    os.mkdir("data")

if __name__ == "__main__":
    ctl = Controller()
    ctl.main_run()
