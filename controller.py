import os
from datetime import datetime

from pydantic import ValidationError

from view import View
from models import Player, PlayersDb, Tournament, TournamentsDb, TournamentPlayer, Round


class Controller:
    def __init__(self) -> None:
        self.actual_tournament = None
        self.view = View()
        self.players_db = PlayersDb()
        self.tournament_db = TournamentsDb()

    def register_new_player(self) -> None:
        loop = True
        while loop:
            user_input = self.view.new_player()
            try:
                player = Player(**user_input)
            except ValidationError as e:
                field_error = e.errors()[0].get("loc")[0]
                self.view.view_error_message(f"Error in field '{field_error}'")
            else:
                if self.players_db.save_new_player(player):
                    self.view.view_message(f"New player id '{player.id}' saved !")
                else:
                    self.view.view_error_message(f"Player id '{player.id}' already exist !")
            if not self.view.confirm("Continue to enter new player ?"):
                    loop = False

    def players_register(self) -> None:
        players = self.players_db.get_all_players()
        list_of_players = [player.__dict__ for player in players]
        list_of_players.sort(key=lambda player: player["lastname"])
        self.view.view_table("Registered players", list_of_players)

    def create_new_tournament(self) -> None:
        tournaments_name = [tournament.name for tournament in self.tournament_db.get_all_tournaments()]
        run = True
        while run:
            user_input = self.view.create_tournament()
            if user_input.get("name") not in tournaments_name:
                rounds = user_input.get("number_of_round")
                if rounds.isnumeric() or not rounds:
                    rounds = int(rounds) if rounds else 4
                    if 4 <= rounds <= 10:   
                        user_input["number_of_round"] = rounds
                        tournament = Tournament(**user_input)
                        self.tournament_db.save(tournament)
                        self.view.view_message(f"New tournament '{user_input.get('name')}' created !")
                        if self.view.confirm("Add players to tournament ?"):
                            self.actual_tournament = tournament
                            self.add_tournament_player()
                        run = False
                    else:
                        self.view.view_error_message("Round must be in range 4 to 10 !")
                else:
                    self.view.view_error_message("Round must be an integer in range 4 to 10 !")
            else:
                self.view.view_error_message(f"Tournament Name '{user_input.get('name')}' already exist !")

    def select_tournament(self) -> bool:
        if self.tournament_db.get_all_tournaments():
            tournaments = self.tournament_db.get_all_tournaments()
            selection = {}
            for key, tournament in enumerate(tournaments):
                selection[str(key)] = tournament
            choice = self.view.input_menu(selection)
            self.actual_tournament = selection.get(choice)
            return True
        else:
            self.view.view_error_message("No tournament !")
            return False

    def all_tournaments(self) -> None:
        tournaments = self.tournament_db.get_all_tournaments()
        table = []
        for tournament in tournaments:
            table.append({
                "Name": tournament.name,
                "Place": tournament.place,
                "Start": tournament.start[1] if tournament.start[0] else "No started !",
                "End": tournament.end[1] if tournament.end[0] else "No started !"
            })
        self.view.view_table("All tournaments", table)

    def start_tournament(self): # todo: a faire
            date = datetime.now().strftime("%d-%m-%Y")
            self.actual_tournament.start = (True, date)
            self.tournament_db.save(self.actual_tournament)

            # create round
            if not self.actual_tournament:
                pass


    def add_tournament_player(self) -> None:
        id_in_tournament = [player.id for player in self.actual_tournament.players]
        players = []
        for player in self.players_db.get_all_players():
            if player.id not in id_in_tournament:
                players.append(TournamentPlayer(player.id, player.lastname, player.firstname))
                
        loop = True
        while loop:
            if players:
                if not self.actual_tournament.start[0]:
                    players.sort(key=lambda player: player.lastname)

                    selection = {}
                    for key, player in enumerate(players):
                        selection[str(key)] = player
                    choice = self.view.input_menu(selection)

                    if choice in selection.keys():
                        self.actual_tournament.players.append(players.pop(int(choice)))
                        self.tournament_db.save(self.actual_tournament)
                        self.view.view_message(f"Player: '{player}' added !")
                        self.view.view_message(f"players in this tournament: {len(self.actual_tournament.players)}")
                        if len(self.actual_tournament.players) % 2 == 1:
                            self.view.view_error_message("You need to add player for pairing players !")
                    else:
                        self.view.view_error_message("Bad choice !")

                    if not self.view.confirm("add new player ?"):
                        loop = False
                else:
                    self.view.view_error_message("don't add player in started tournament !")
                    loop = False
            else:
                self.view.view_error_message("All players in tournament or no players in register !")
                loop = False

    def tournament_header(self) -> None:
        data = [{
            "Tournament name": self.actual_tournament.name,
            "Place": self.actual_tournament.place,
            "Start date": self.actual_tournament.start[1] if self.actual_tournament.start[0] else "No started !",
            "End date": self.actual_tournament.end[1] if self.actual_tournament.end[0] else "No started !" 
        }]
        self.view.view_table("tournament", data)

    def get_tournament_players(self) -> None:
        players = [player.__dict__ for player in self.actual_tournament.players]
        players.sort(key=lambda player: player["lastname"])
        self.view.view_table("Players in tournament", players)

    def rounds_and_matchs(self): # todo: a faire
        pass

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
                                self.register_new_player()
                            case "2":
                                self.players_register()
                            case "3":
                                choice = "1"
                                loop_1 = False
                case "2":
                    loop_1 = True
                    while loop_1:
                        choice = self.view.tournaments_menu()
                        match choice:
                            case "1":
                                self.create_new_tournament()
                            case "2":
                                loop_2 = True if self.select_tournament() else False
                                while loop_2:
                                    choice = self.view.tournament_menu()
                                    match choice:
                                        case "1":
                                            self.start_tournament()
                                        case "2":
                                            self.add_tournament_player()
                                        case "3":
                                            self.tournament_header()
                                        case "4":
                                            self.get_tournament_players()
                                        case "5":
                                            self.rounds_and_matchs()
                                        case "6":
                                            choice = 2
                                            loop_2 = False
                            case "3":
                                self.all_tournaments()
                            case "4":
                                choice = 2
                                loop_1 = False
                case "3":
                    run = False


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.mkdir("data")
    ctl = Controller()
    ctl.run()