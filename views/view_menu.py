from views.view import View
from controllers.players_controller import PlayerCtl
from controllers.tournaments_controller import TournamentCtl


class Controller:
    def __init__(self) -> None:
        self.run = True
        self.view = View()
        self.players_ctl = PlayerCtl()
        self.tournament_ctl = TournamentCtl()

    def main_menu(self) -> None:
        menu = {
            "1": "Players",
            "2": "Tournaments",
            "3": "Quit"
        }
        choice = self.view.input_menu(menu)
        match choice:
            case "1":
                self.players_menu()
            case "2":
                self.tournaments_menu()
            case "3":
                self.run = False

    def players_menu(self) -> None:
        menu = {
            "1": "Add new player to register",
            "2": "View players register",
            "3": "Back"
        }
        choice = self.view.input_menu(menu)
        match choice:
            case "1":
                self.players_ctl.register_new_player()
                self.players_menu()
            case "2":
                self.players_ctl.players_register()
                self.players_menu()
            case "3":
                self.main_menu()

    def tournaments_menu(self) -> None:
        menu = {
            "1": "Create new tournament",
            "2": "Select tournament",
            "3": "View all tournaments",
            "4": "Back"
        }
        choice = self.view.input_menu(menu)
        match choice:
            case "1":
                if choice:
                    self.tournament_ctl.create_new_tournament()
                self.tournaments_menu()
            case "2":
                if self.tournament_ctl.select_tournament():
                    self.selected_tournament_menu()
                else:
                    self.tournaments_menu()
            case "3":
                self.tournament_ctl.all_tournaments()
                self.tournaments_menu()
            case "4":
                self.main_menu()

    def selected_tournament_menu(self) -> None:
        menu = {
            "1": "Start tournament",
            "2": "Add player to tournament",
            "3": "Add or modify comment",
            "4": "View tournament name, place and date",
            "5": "View tournament players",
            "6": "View rounds and matches",
            "7": "Back"
        }
        choice = self.view.input_menu(menu)
        match choice:
            case "1":
                self.tournament_ctl.start_tournament()
                self.selected_tournament_menu()
            case "2":
                self.tournament_ctl.add_tournament_player()
                self.selected_tournament_menu()
            case "3":
                self.tournament_ctl.add_tournament_comment()
                self.selected_tournament_menu()
            case "4":
                self.tournament_ctl.tournament_header()
                self.selected_tournament_menu()
            case "5":
                self.tournament_ctl.get_tournament_players()
                self.selected_tournament_menu()
            case "6":
                self.tournament_ctl.rounds_and_matches()
                self.selected_tournament_menu()
            case "7":
                self.tournaments_menu()

    def main_run(self) -> None:
        while self.run:
            self.main_menu()
