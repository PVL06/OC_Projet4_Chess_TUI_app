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
        self.rounds = []
        self.actual_round = 0
        self.start = (False, "")
        self.end = (False, "")

    def __str__(self):
        return f"{self.name}, {self.place}"


class TournamentsDb: # todo: finsh for rounds data on serialize and deserialize
    def __init__(self) -> None:
        self.db = TinyDB('data/tournaments.json', indent=4)
        self.query = Query()

    def save(self, tournament: Tournament) -> None:
        tournament_serialized = self.serialize(tournament)
        if self.db.search(self.query.name.matches(tournament.name)):
            self.db.update(tournament_serialized, self.query.name == tournament.name)
        else:
            self.db.insert(tournament_serialized)

    def get_tournament(self, name) -> Tournament | None:
        data = self.db.search(self.query.name.matches(name))[0]
        if data:
            return self.deserialize(data)
        return None
    
    def get_all_tournaments(self) -> list[Tournament]:
        return [self.deserialize(data) for data in self.db.all()]

    @staticmethod
    def deserialize(data: dict) -> Tournament: # todo: finsh for rounds data
        # Convert DB dict to object Tournament
        tournament = Tournament(data.get("name"), data.get("place"), data.get("number_of_round"))
        tournament.players = [TournamentPlayer(**player) for player in data.get("players")]
        tournament.rounds = [] # todo: a finir (voir objets a l'interieur)
        tournament.actual_round = data.get('actual_round')
        tournament.start = data.get('start')
        tournament.end = data.get('end')
        return tournament

    @staticmethod
    def serialize(object: Tournament) -> dict: # todo: finsh for rounds data
        # Convert tournament object to dict for DB
        tournament = {
            "name": object.name,
            "place": object.place,
            "players": [player.__dict__ for player in object.players],
            "rounds": [], # todo: a finir
            "actual_round": object.actual_round,
            "start": object.start,
            "end": object.end
        }
        return tournament


class TournamentPlayer:
    def __init__(self, id, lastname, firstname, score=0) -> None:
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.score = str(score)

    def get_player(self):
        self.player = [(self.id, self.lastname, self.firstname), self.score]

    def __str__(self):
        return f"{self.id} : {self.lastname}, {self.firstname}"
    

class Round:
    def __init__(self, round: str) -> None:
        self.round = round
        self.matchs = []
