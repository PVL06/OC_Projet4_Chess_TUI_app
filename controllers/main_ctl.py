from views.view import View
from controllers.players_ctl import PlayerCtl
from controllers.tournaments_ctl import TournamentsCtl


class Controller:
    def __init__(self):
        self.view = View()
        self.players_ctl = PlayerCtl()
        self.tournaments_ctl = TournamentsCtl()

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
                    self.players_ctl.players_menu()
                case "2":
                    self.tournaments_ctl.tournaments_menu()
                case "3":
                    running = False
                case _:
                    self.view.view_message("Invalid input !", error=True)
