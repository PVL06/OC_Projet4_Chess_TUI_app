from pydantic import ValidationError

from view import Viewer
from models import Player, RegisteredPlayers


class Controller:
    def __init__(self) -> None:
        self.registered_players = RegisteredPlayers()
        self.viewer = Viewer()

    def register_new_player(self):
        fields = {
            "id": "Player id (ex: DF12345): ",
            "firstname": "Firstname: ",
            "lastname": "Lastname: ",
            "date_of_birth": "Date of birth (dd/mm/yyyy): "
            }
        user_input = self.viewer.user_input(fields)
        try:
            player = Player(**user_input)
        except ValidationError as e:
            field_error = e.errors()[0].get("loc")[0]
            self.viewer.view_error_message(f"Error in field '{field_error}'")
        else:
            if self.registered_players.save_player(player):
                self.viewer.view_message(f"New player id[{player.id}] saved !")
            else:
                self.viewer.view_error_message(f"Player id[{player.id}] already exist !")

    def view_regitered_players(self):
        players = self.registered_players.get_players()
        list_of_players = [player.__dict__ for player in players]
        self.viewer.view_table(list_of_players, "Registered players")

    def main(self):
        run = True
        while run:
            menu = {"1": "Add new player", "2": "View players", "3": "Quit"}
            choice = self.viewer.input_menu(menu)
            if choice == "1":
                self.register_new_player()
            elif choice == "2":
                self.view_regitered_players()
            elif choice == "3":
                run = False


ctl = Controller()
ctl.main()