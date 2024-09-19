from views.view import View
from controllers.players_controller import PlayerCtl
from controllers.tournaments_controller import TournamentCtl


class Controller:
    def __init__(self) -> None:
        self.actual_tournament = None
        self.view = View()
        self.players_ctl = PlayerCtl()
        self.tournament_ctl = TournamentCtl()

    def run(self):
        run = True
        while run:
            choice = self.view.main_menu()
            match choice:
                case "1":
                    loop_1 = True
                    while loop_1:
                        choice = self.view.players_menu()
                        match choice:
                            case "1":
                                self.players_ctl.register_new_player()
                            case "2":
                                self.players_ctl.players_register()
                            case "3":
                                choice = "1"
                                loop_1 = False
                case "2":
                    loop_1 = True
                    while loop_1:
                        choice = self.view.tournaments_menu()
                        match choice:
                            case "1":
                                self.tournament_ctl.create_new_tournament()
                            case "2":
                                loop_2 = True if self.tournament_ctl.select_tournament() else False
                                while loop_2:
                                    choice = self.view.tournament_menu()
                                    match choice:
                                        case "1":
                                            self.tournament_ctl.start_tournament()
                                        case "2":
                                            self.tournament_ctl.add_tournament_player()
                                        case "3":
                                            self.tournament_ctl.tournament_header()
                                        case "4":
                                            self.tournament_ctl.get_tournament_players()
                                        case "5":
                                            self.tournament_ctl.rounds_and_matches()
                                        case "6":
                                            loop_2 = False
                            case "3":
                                self.tournament_ctl.all_tournaments()
                            case "4":
                                choice = 2
                                loop_1 = False
                case "3":
                    run = False
