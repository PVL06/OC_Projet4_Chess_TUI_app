from pydantic import ValidationError

from views.view import View
from models.players_model import PlayersDb, Player


class PlayerCtl:
    def __init__(self) -> None:
        self.view = View()
        self.players_db = PlayersDb()

    def register_new_player(self) -> None:
        loop = True
        while loop:
            fields = {
                "id": "Player id (ex: DF12345): ",
                "firstname": "Firstname: ",
                "lastname": "Lastname: ",
                "date_of_birth": "Date of birth (dd/mm/yyyy): "
            }
            user_input = self.view.user_input(fields)
            user_input["lastname"] = user_input["lastname"].capitalize()
            user_input["firstname"] = user_input["firstname"].capitalize()
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
        self.view.view_table("Registered players", list_of_players)
