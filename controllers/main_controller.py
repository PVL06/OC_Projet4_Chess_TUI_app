from views.view import View
from controllers.players_controller import PlayerCtl


class Controller:
    def __init__(self):
        self.view = View()
        self.player_ctl = PlayerCtl()

    def start(self):
        running = True
        while running:
            menu = [
                ("1", "Player"),
                ("2", "Tournament"),
                ("3", "Quit")
            ]
            choice = self.view.input_menu(menu)
            match choice:
                case "1":
                    self.player_ctl.players_menu()
                case "2":
                    pass
                case "3":
                    running = False
                case _:
                    self.view.view_message("Invalid input !", error=True)
