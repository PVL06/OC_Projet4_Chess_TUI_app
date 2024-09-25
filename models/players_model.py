from tinydb import TinyDB, Query
from pydantic import BaseModel, Field


class Player(BaseModel):
    id: str = Field(pattern=r"^([A-Z]{2})([0-9]{5})$")
    lastname: str = Field(pattern=r"^[a-zA-Z -]*$", min_length=2)
    firstname: str = Field(pattern=r"^[a-zA-Z -]*$", min_length=2)
    date_of_birth: str = Field(pattern=r"^(0[1-9]|[12][0-9]|3[01])\/(0[0-9]|1[012])\/([0-9]{4})$")

    def __str__(self) -> str:
        return f"{self.id} {self.lastname} {self.firstname}"


class PlayersDb:
    def __init__(self) -> None:
        self.db = TinyDB('data/players.json', indent=4)
        self.query = Query()

    def save_new_player(self, player: Player) -> bool:
        if not self.db.search(self.query.id.matches(player.id)):
            self.db.insert(player.__dict__)
            return True
        return False

    def get_player(self, player_id: str) -> Player | None:
        player = self.db.search(self.query.id == player_id)
        if player:
            return Player(**player[0])
        return None

    def get_player_doc_id(self, player_id: str) -> int | None:
        if self.db.search(self.query.id.matches(player_id)):
            player = self.db.get(self.query.id == player_id)
            return player.doc_id
        return None

    def update_player(self, player: Player, doc_id: int) -> bool:
        if self.db.update(player.__dict__, doc_ids=[doc_id]):
            return True
        return False

    def remove_player(self, player_id: str) -> bool:
        if self.db.remove(self.query.id.matches(player_id)):
            return True
        return False

    def get_all_players(self) -> list[Player]:
        players = [Player(**player) for player in self.db]
        players.sort(key=lambda player: player.lastname)
        return players
