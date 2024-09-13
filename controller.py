from pydantic import ValidationError

from view import View
from models import Player, PlayersDb, Tournament, TournamentsDb, PlayerPoint, Round


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
                if not self.view.confirm("Retry ?"):
                    loop = False
            else:
                if self.players_db.save_new_player(player):
                    self.view.view_message(f"New player id '{player.id}' saved !")
                else:
                    self.view.view_error_message(f"Player id '{player.id}' already exist !")

    def players_register(self) -> None:
        players = self.players_db.get_all_players()
        list_of_players = [player.__dict__ for player in players]
        list_of_players.sort(key=lambda player: player["lastname"])
        self.view.view_table(list_of_players, "Registered players")

    def all_tournaments(self): # todo: a finir pour vue dans un tableau
        tournaments = self.tournament_db.get_all_tournaments()
        for tournament in tournaments:
            print(tournament.name)

    def select_tournament(self): # todo: a faire
        pass


    def create_new_tournament(self) -> None: # todo: check if tournament name not exist
        run = True
        while run:
            user_input = self.view.create_tournament()
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


    def add_tournament_player(self) -> None:
        players = self.players_db.get_all_players()
        loop = True
        while loop:
            if not self.actual_tournament.start[0]:
                players.sort(key=lambda player: player.lastname)
                menu = {}
                for i in range(len(players)):
                    menu[str(i)] = players[i]
                choice = self.view.input_menu(menu)

                if choice in menu.keys():
                    player = menu.get(choice)
                    self.actual_tournament.players.append(player)
                    self.tournament_db.save(self.actual_tournament)
                    self.view.view_message(f"Player: '{player}' added !")
                    self.view.view_message(f"{len(self.actual_tournament.players)} players in this tournament")
                else:
                    self.view.view_error_message("Bad choice !")

                if not self.view.confirm("add new player ?"):
                        loop = False


            else:
                self.view.view_error_message("don't add player in started tournament !")

    def run(self):
        run = True
        while run:
            choice = self.view.main_menu()
            if choice == "1":
                self.register_new_player()
            elif choice == "2":
                self.players_register()
            elif choice == "3":
                self.create_new_tournament()
            elif choice == "4":
                self.all_tournaments()
            elif choice == "5":
                run = False


ctl = Controller()
ctl.run()