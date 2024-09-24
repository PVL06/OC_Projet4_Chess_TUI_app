import os

from views.view_menu import MenuCtl

if not os.path.exists("data"):
    os.mkdir("data")

if __name__ == "__main__":
    ctl = MenuCtl()
    ctl.main_run()
