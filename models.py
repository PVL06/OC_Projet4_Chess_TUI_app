from tinydb import TinyDB, Query
from pydantic import BaseModel, Field


class Player(BaseModel):
    id: str = Field(pattern=r"^([A-Z]{2})([0-9]{5})$")
    firstname: str = Field(pattern=r"^[a-zA-Z -]*$", min_length=2)
    lastname: str = Field(pattern=r"^[a-zA-Z -]*$", min_length=2)
    date_of_birth: str = Field(pattern=r"^(0[1-9]|[12][0-9]|3[01])\/(0[0-9]|1[012])\/([0-9]{4})$")

    def __str__(self) -> str:
        return f"{self.id} {self.firstname} {self.lastname}"


class PlayersDb:
    def __init__(self) -> None:
        self.db = TinyDB('data/players.json', indent=4)
        self.query = Query()

    def save_new_player(self, player: Player) -> bool:
        if not self.db.search(self.query.id.matches(player.id)):
            self.db.insert(player.__dict__)
            return True
        return False

    def get_player(self, id) -> Player | None:
        player = self.db.search(self.query.id == id)
        if player:
            return Player(**player[0])
        return None

    def get_all_players(self) -> list[Player]:
        players = [Player(**player) for player in self.db]
        return players
    

class Tournament:
    def __init__(self, name: str, place: str, number_of_round=4) -> None:
        self.name = name
        self.place = place
        self.number_of_round = number_of_round
        self.players = []
        self.round = []
        self.actual_round = 0
        self.start = (False, "")
        self.end = (False, "")

    def __str__(self):
        return f"{self.name}, {self.place}"


class TournamentsDb:
    def __init__(self) -> None:
        self.db = TinyDB('data/tournaments.json', indent=4)
        self.query = Query()

    def save(self, tournament: Tournament) -> None:
        if self.db.search(self.query.name.matches(tournament.name)):
            self.db.update(tournament.__dict__, self.query.name == tournament.name)
        else:
            self.db.insert(tournament.__dict__)

    def get_tournament(self, name) -> Tournament | None:
        data = self.db.search(self.query.name.matches(name))[0]
        if data:
            return self.convert_data(data)
        return None
    
    def get_all_tournaments(self) -> list[Tournament]:
        return [self.convert_data(data) for data in self.db.all()]

    @staticmethod
    def convert_data(data) -> Tournament:
        tournament = Tournament(data.get('name'), data.get("place"))
        for key, value in data.items():
            tournament.key = value
        return tournament


class PlayerPoint:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.point = 0
    
    def get_player_point(self) -> list[Player, int]:
        return [self.player, self.point]
    
    def add_point(self, point: int):
        self.point += point

    def __str__(self):
        return f"{self.player}, {self.point}"

    
class Round:
    def __init__(self, round: str) -> None:
        self.round = round
        self.matchs = []
