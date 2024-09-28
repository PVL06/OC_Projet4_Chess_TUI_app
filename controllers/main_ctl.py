from views.view import View
from models.tournaments_model import Tournament
from controllers.players_ctl import PlayerCtl
from controllers.tournaments_ctl import TournamentsCtl, ActualTournament


class Controller:
    def __init__(self):
        self.view = View()
        self.players_ctl = PlayerCtl()
        self.tournaments_ctl = TournamentsCtl()
        self.actual_tournament = ActualTournament()

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
                    self.players_menu()
                case "2":
                    self.tournaments_menu()
                case "3":
                    running = False
                case _:
                    self.view.view_message("Invalid input !", error=True)

    def players_menu(self) -> None:
        running = True
        while running:
            menu = [
                ("1", "Add new player to register"),
                ("2", "Modify player"),
                ("3", "Delete player"),
                ("4", "View players register"),
                ("5", "Back")
            ]
            choice = self.view.input_menu(menu)
            match choice:
                case "1":
                    self.players_ctl.register_new_player()
                case "2":
                    self.players_ctl.modify_player()
                case "3":
                    self.players_ctl.delete_player()
                case "4":
                    self.players_ctl.players_register()
                    self.view.enter_continue()
                case "5":
                    running = False
                case _:
                    self.view.view_message("Invalid input !", error=True)

    def tournaments_menu(self):
        running = True
        while running:
            menu = [
                ("1", "Create new tournament"),
                ("2", "Delete tournament"),
                ("3", "Select tournament"),
                ("4", "View all tournaments"),
                ("5", "Back")
            ]
            choice = self.view.input_menu(menu)
            match choice:
                case "1":
                    self.tournaments_ctl.create_new_tournament()
                case "2":
                    self.tournaments_ctl.delete_tournament()
                case "3":
                    tournament = self.tournaments_ctl.select_tournament()
                    if tournament:
                        self.selected_tournament_menu(tournament)
                case "4":
                    self.tournaments_ctl.all_tournaments()
                case "5":
                    running = False
                case _:
                    self.view.view_message("Invalid input !", error=True)

    def selected_tournament_menu(self, tournament: Tournament) -> None:
        self.actual_tournament.actual_tournament = tournament
        running = True
        while running:
            menu = [
                ("1", "Start tournament"),
                ("2", "Add player in this tournament"),
                ("3", "Remove player in this tournament"),
                ("4", "Add or modify comment"),
                ("5", "View tournament name, place and status"),
                ("6", "View tournament players"),
                ("7", "View rounds and matches"),
                ("8", "View tournament result"),
                ("9", "Back")
            ]
            choice = self.view.input_menu(menu)
            match choice:
                case "1":
                    self.actual_tournament.start_tournament()
                case "2":
                    self.actual_tournament.add_tournament_player()
                case "3":
                    self.actual_tournament.remove_tournament_player()
                case "4":
                    self.actual_tournament.add_tournament_comment()
                case "5":
                    self.actual_tournament.view_tournament_header()
                case "6":
                    self.actual_tournament.view_tournament_players()
                case "7":
                    self.actual_tournament.rounds_and_matches()
                case "8":
                    self.actual_tournament.show_players_result()
                case "9":
                    running = False
                case _:
                    self.view.view_message("Invalid input !", error=True)
