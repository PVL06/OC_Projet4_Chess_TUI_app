from tinydb import TinyDB, Query


TOURNAMENTS_DIR = "data/tournaments.json"


class Round:
    def __init__(self, round_number: int) -> None:
        self.name = f"Round {str(round_number)}"
        self.round_start = ""
        self.round_stop = ""
        self.matches = []


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
        self.combination = []

    def __str__(self):
        return f"{self.name}, {self.place}"


class TournamentsDb:
    """
    Class that manages the JSON database for tournaments
    Functionality to save or remove tournament and get all tournaments
    """

    def __init__(self) -> None:
        self.db = TinyDB(TOURNAMENTS_DIR, indent=4)
        self.query = Query()

    def save(self, tournament: Tournament) -> None:
        serialized_tournament = tournament.__dict__
        if self.db.search(self.query.name.matches(tournament.name)):
            self.db.update(serialized_tournament, self.query.name == tournament.name)
        else:
            self.db.insert(serialized_tournament)

    def delete_tournament(self, name: str) -> bool:
        if self.db.remove(self.query.name.matches(name)):
            return True
        return False

    def get_all_tournaments(self) -> list[Tournament]:
        tournaments = []
        for tournament in self.db.all():
            new = self.deserialize(tournament)
            tournaments.append(new)
        return tournaments

    @staticmethod
    def deserialize(data: dict) -> Tournament:
        """Convert DB dict to object Tournament"""

        tournament = Tournament(data.get("name"), data.get("place"), data.get("number_of_round"))
        tournament.players = data.get("players")
        tournament.rounds = data.get("rounds")
        tournament.start = data.get("start")
        tournament.end = data.get("end")
        tournament.comment = data.get("comment")
        tournament.combination = data.get("combination")
        return tournament
