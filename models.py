import os
import json

from pydantic import BaseModel, Field
from pydantic import ValidationError


class Player(BaseModel):
    id: str = Field(pattern=r"^([A-Z]{2})([0-9]{5})$")
    firstname: str = Field(pattern=r"^[A-Z]*$", min_length=2)
    lastname: str = Field(pattern=r"^[A-Z]*$", min_length=2)
    date_of_birth: str = Field(pattern=r"^(0[1-9]|[12][0-9]|3[01])\/(0[0-9]|1[012])\/([0-9]{4})$")

    def __str__(self) -> str:
        return f"{self.id} {self.firstname} {self.lastname}"
    

class RegisteredPlayers:
    def __init__(self) -> None:
        self.players_file_path = "data/players.json"
        if not os.path.exists("data/"):
            os.mkdir("data")

    def save_player(self, player: Player) -> None:
        if os.path.exists(self.players_file_path):
            with open(self.players_file_path, "r+") as file:
                data = json.load(file)
                data["players"].append(player.__dict__)
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open(self.players_file_path, "w") as file:
                json.dump({'players': [player.__dict__]}, file, indent=4)

    def get_players(self) -> list[Player] | None:
        if os.path.exists(self.players_file_path):
            with open(self.players_file_path, "r") as file:
                data = json.load(file)
                return [Player(**player) for player in data["players"]]
        return None
