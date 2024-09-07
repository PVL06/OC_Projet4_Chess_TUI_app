from pydantic import ValidationError

from view import View
from models import Player, PlayersRegister, Tournament

class CtlPlayers:
    def __init__(self) -> None:
        self.view = View()
        self.players_register = PlayersRegister()

    def register_new_player(self):
        user_input = self.view.new_player()
        try:
            player = Player(**user_input)
        except ValidationError as e:
            field_error = e.errors()[0].get("loc")[0]
            self.viewer.view_error_message(f"Error in field '{field_error}'")
        else:
            if self.players_register.save_player(player):
                self.viewer.view_message(f"New player id '{player.id}' saved !")
            else:
                self.viewer.view_error_message(f"Player id '{player.id}' already exist !")

    #todo: trier par ordre alphabetique
    def register(self):
        players = self.players_register.get_players()
        list_of_players = [player.__dict__ for player in players]
        self.viewer.view_table(list_of_players, "Registered players")


class CtlTournament:
    def __init__(self) -> None:
        self.view = View()
        self.tournament = None

    def new_tournament(self):
        self.create_new_tournament()
        #self.add_players()

    def create_new_tournament(self):
        
        run = True
        while run:
            user_input = self.view.create_tournament()
            rounds = user_input.get("number_of_round")
            if rounds.isnumeric() or not rounds:
                rounds = int(rounds) if rounds else 4
                if 4 <= rounds <= 10:
                    user_input["number_of_round"] = rounds
                    self.view.view_message(f"New tournament '{user_input.get('name')}' created !")
                    run = False
                    self.tournament = Tournament(**user_input)
                else:
                    self.view.view_error_message("Round must be in range 4 to 10 !")
            else:
                self.view.view_error_message("Round must be an integer in range 4 to 10 !")

    def add_players(self):

        self.tournament.add_player()



class Controller:
    def __init__(self) -> None:
        self.view = View()
        self.players = CtlPlayers()
        self.tournament = CtlTournament()

    def run(self):
        run = True
        while run:
            choice = self.view.main_menu()
            if choice == "1":
                self.players.register_new_player()
            elif choice == "2":
                self.players.register()
            elif choice == "3":
                self.tournament.new_tournament()
            elif choice == "4":
                print('all tournament')
            elif choice == "5":
                run = False


ctl = Controller()
ctl.run()