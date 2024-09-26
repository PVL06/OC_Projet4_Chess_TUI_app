from tinydb import TinyDB, Query

from models.players_model import Player


class Tournament:
    def __init__(self, name: str, place: str, number_of_round=4) -> None:
        self.name = name
        self.place = place
        self.number_of_round = number_of_round
        self.players = []
        self.rounds = []
        self.start = ""
        self.end = ""
        self.comment = ""

    def __str__(self):
        return f"{self.name}, {self.place}"


class TournamentsDb:
    def __init__(self) -> None:
        self.db = TinyDB('data/tournaments.json', indent=4)
        self.query = Query()

    def save(self, tournament: Tournament) -> None:
        serialized_tournament = self.serialize(tournament)
        if self.db.search(self.query.name.matches(tournament.name)):
            self.db.update(serialized_tournament, self.query.name == tournament.name)
        else:
            self.db.insert(serialized_tournament)

    def get_all_tournaments(self) -> list[Tournament]:
        tournaments = []
        for tournament in self.db.all():
            new = self.deserialize(tournament)
            tournaments.append(new)
        return tournaments

    @staticmethod
    def deserialize(data: dict) -> Tournament:
        # Convert DB dict to object Tournament
        tournament = Tournament(data.get("name"), data.get("place"), data.get("number_of_round"))
        tournament.players = [Player(**player) for player in data.get("players")]
        tournament.rounds = data.get("rounds")
        tournament.start = data.get("start")
        tournament.end = data.get("end")
        tournament.comment = data.get("comment")
        return tournament

    @staticmethod
    def serialize(tournament: Tournament) -> dict:
        # Convert tournament object to dict for DB
        tournament = {
            "name": tournament.name,
            "place": tournament.place,
            "number_of_round": tournament.number_of_round,
            "players": [player.__dict__ for player in tournament.players],
            "rounds": tournament.rounds,
            "start": tournament.start,
            "end": tournament.end,
            "comment": tournament.comment
        }
        return tournament
