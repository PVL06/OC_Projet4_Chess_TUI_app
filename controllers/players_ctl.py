from pydantic import ValidationError

from views.view import View
from models.players_model import PlayersDb, Player
from controllers.utils import Utils


class PlayerCtl:
    def __init__(self) -> None:
        self.view = View()
        self.players_db = PlayersDb()
        self.utils = Utils()

    def register_new_player(self) -> None:
        fields = {
            "id": "Player id (ex: DF12345): ",
            "firstname": "Firstname: ",
            "lastname": "Lastname: ",
            "date_of_birth": "Date of birth (dd/mm/yyyy): "
        }
        user_input = self.view.multiple_inputs(fields)
        if player := self._create_player(user_input):
            if self.players_db.save_new_player(player):
                self.view.view_message(f"New player id '{player.id}' saved !")
            else:
                self.view.view_message(f"Player id '{player.id}' already exist !", error=True)

    def modify_player(self) -> None:
        players = self.players_db.get_all_players()
        if player := self.utils.players_selection(players):
            doc_id = self.players_db.get_player_doc_id(player.id)
            self.view.view_message("Press just enter for the same value or input new value")
            player = player.__dict__
            updated = True
            for field, value in player.items():
                if user_input := self.view.simple_input(f"{field} '{value}': "):
                    if field == "id" and user_input in [player.id for player in self.players_db.get_all_players()]:
                        self.view.view_message("Id is already used !", error=True)
                        updated = False
                        break
                    else:
                        player[field] = user_input

            player = self._create_player(player)
            if player and updated:
                if self.players_db.update_player(player, doc_id):
                    self.view.view_message(f"Player updated -> {player.__str__()}")
                else:
                    self.view.view_message(f"Error, player no updated !", error=True)
            else:
                self.view.view_message("No players", error=True)

    def delete_player(self) -> None:
        players = self.players_db.get_all_players()
        if player := self.utils.players_selection(players):
            if self.view.confirm(f"Are you sure to remove player: {player.__str__()}"):
                self.players_db.remove_player(player.id)
                self.view.view_message(f"Player deleted: {player.__str__()}")

    def players_register(self) -> None:
        if players := self.players_db.get_all_players():
            list_of_players = [player.__dict__ for player in players]
            if not self.view.table_view("Registered players", list_of_players, ):
                self.view.view_message("No data", error=True)

    def _create_player(self, data: dict) -> Player | None:
        try:
            data["lastname"] = data["lastname"].capitalize()
            data["firstname"] = data["firstname"].capitalize()
            player = Player(**data)
        except ValidationError as e:
            field_error = e.errors()[0].get("loc")[0]
            self.view.view_message(f"Invalid input on field: {field_error}", error=True)
        else:
            return player
