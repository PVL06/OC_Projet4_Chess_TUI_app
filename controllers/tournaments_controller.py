from datetime import datetime
import random
import itertools


from views.view import View
from models.tournaments_model import Tournament, TournamentsDb
from models.players_model import PlayersDb, Player


class Rounds:
    def __init__(self, players: list[Player]) -> None:
        self.players_score = [[player, 0.0] for player in players]
        self.all_pairs = list(itertools.combinations(self.players_score, 2))
        self.used_pairs = []
        self.start_round = ""
        self.end_round = ""
        self.results = []

    def get_player_score(self, player_id: str) -> list | None:
        for i in range(len(self.players_score)):
            if player_id == self.players_score[i][0].id:
                return self.players_score[i]
        return None

    def get_matches(self) -> list[([Player, int], [Player, int])]:
        self.all_pairs.sort(key=lambda players_score: abs(players_score[0][1] - players_score[1][1]))
        players_id = [player[0].id for player in self.players_score]

        matches = []
        for combination in self.all_pairs:
            conditions = [
                combination not in self.used_pairs,
                combination[0][0].id in players_id,
                combination[1][0].id in players_id
            ]
            if all(conditions):
                players_id.remove(combination[0][0].id)
                players_id.remove(combination[1][0].id)
                matches.append(combination)
                self.all_pairs.remove(combination)

        if players_id:
            for i in range(0, len(players_id), 2):
                player1 = self.get_player_score(players_id[i])
                player2 = self.get_player_score(players_id[i+1])
                if player1 and player2:
                    matches.append((player1, player2))

        return matches

    @staticmethod
    def get_matches_table(matches):
        matches_table = []
        for index, match in enumerate(matches):
            table_row = {
                "key": str(index + 1),
                "player 1 (WHITE)": match[0][0].__str__(),
                "player 1 score": str(match[0][1]),
                "": "VS",
                "player 2 (BLACK)": match[1][0].__str__(),
                "player 2 score": str(match[1][1]),
                "Winner": ""
            }
            matches_table.append(table_row)
        return matches_table

    def add_player_point(self, player_id: str, point: float) -> None:
        for i in range(len(self.players_score)):
            if player_id == self.players_score[i][0].id:
                self.players_score[i][1] += point


class TournamentCtl:
    def __init__(self) -> None:
        self.actual_tournament = None
        self.view = View()
        self.players_db = PlayersDb()
        self.tournament_db = TournamentsDb()

    def create_new_tournament(self) -> None:
        tournaments_name = [tournament.name for tournament in self.tournament_db.get_all_tournaments()]
        run = True
        while run:
            fields = {
                "name": "Tournament name: ",
                "place": "Tournament place: ",
                "number_of_round": "Number of round (4 round if no value): "
            }
            user_input = self.view.user_input(fields)

            if user_input.get("name") not in tournaments_name:
                rounds_number = user_input.get("number_of_round")
                if rounds_number.isnumeric() or not rounds_number:
                    rounds_number = int(rounds_number) if rounds_number else 4
                    if 4 <= rounds_number <= 10:
                        user_input["number_of_round"] = rounds_number
                        tournament_data = {
                            "players": [],
                            "rounds": [],
                            "start": (False, ""),
                            "end": (False, ""),
                            "comment": ""
                        }
                        user_input.update(tournament_data)
                        tournament = Tournament(**user_input)
                        self.tournament_db.save(tournament)
                        self.view.view_message(f"New tournament '{user_input.get('name')}' created !")
                        if self.view.confirm("Add players to tournament ?"):
                            self.actual_tournament = tournament
                            self.add_tournament_player()
                        run = False
                    else:
                        self.view.view_error_message("Round must be in range 4 to 10 !")
                else:
                    self.view.view_error_message("Round must be an integer in range 4 to 10 !")
            else:
                self.view.view_error_message(f"Tournament Name '{user_input.get('name')}' already exist !")

    def add_tournament_player(self) -> None:
        players_db = self.players_db.get_all_players()

        loop = True
        while loop:
            players_tournament_id = [player.id for player in self.actual_tournament.players]
            players_available = [player for player in players_db if player.id not in players_tournament_id]
            if players_available:
                if not self.actual_tournament.start[0]:

                    selection = {}
                    for key, player in enumerate(players_available):
                        selection[str(key)] = f"{player.id}: {player.lastname}, {player.firstname}"
                    choice = self.view.input_menu(selection)

                    if choice in selection.keys():
                        player = players_available[int(choice)]
                        self.actual_tournament.players.append(player)
                        self.tournament_db.save(self.actual_tournament)
                        self.view.view_message(f"Player: '{player.__str__()}' added !")
                        self.view.view_message(f"players in this tournament: {len(self.actual_tournament.players)}")
                        if len(self.actual_tournament.players) % 2 == 1:
                            self.view.view_error_message("You need to add player for pairing players !")
                    else:
                        self.view.view_error_message("Bad choice !")

                    if not self.view.confirm("add new player ?"):
                        loop = False
                        if self.view.confirm("Do you start the tournament ?"):
                            self.start_tournament()
                else:
                    self.view.view_error_message("don't add player in started tournament !")
                    loop = False
            else:
                self.view.view_error_message("All players in tournament or no players in register !")
                loop = False

    def select_tournament(self) -> bool:
        if tournaments := self.tournament_db.get_all_tournaments():
            selection = {}
            for key, tournament in enumerate(tournaments):
                selection[str(key)] = tournament
            choice = self.view.input_menu(selection)
            if choice:
                self.actual_tournament = selection.get(choice)
                return True
        else:
            self.view.view_error_message("No tournament !")
        return False

    def all_tournaments(self) -> None:
        tournaments = self.tournament_db.get_all_tournaments()
        table = []
        for tournament in tournaments:
            table.append({
                "Name": tournament.name,
                "Place": tournament.place,
                "Start": tournament.start[1] if tournament.start[0] else "No started !",
                "End": tournament.end[1] if tournament.end[0] else "No started !"
            })
        self.view.view_table("All tournaments", table)

    @staticmethod
    def update_scores(rounds: Rounds, round_table) -> None:
        for line in round_table:
            match line.get("Winner"):
                case "0":
                    rounds.add_player_point(line.get("player 1 (WHITE)").split(" ")[0], 0.5)
                    rounds.add_player_point(line.get("player 2 (BLACK)").split(" ")[0], 0.5)
                case "1":
                    rounds.add_player_point(line.get("player 1 (WHITE)").split(" ")[0], 1)
                case "2":
                    rounds.add_player_point(line.get("player 2 (BLACK)").split(" ")[0], 1)

    def start_round(self, rounds: Rounds, round_number: int) -> None:
        round_title = f"Round {round_number}/{self.actual_tournament.number_of_round}"
        matches = rounds.get_matches()
        round_table = rounds.get_matches_table(matches)
        rounds.results = [False] * len(matches)

        self.view.view_table(round_title, round_table)
        self.view.simple_input(f"Start round {round_number} (press enter) ?")
        rounds.start_round = datetime.now().strftime("%d-%m-%Y %H:%M")
        round_title += f"  Start: {rounds.start_round}"

        selection = [i+1 for i in range(len(matches))]
        while not all(rounds.results):
            self.view.view_table(round_title, round_table)
            if selected_match := self.view.select_int_input("enter match number: ", selection):
                menu = {
                    "0": "draw",
                    "1": "player 1 win",
                    "2": "player 2 win"
                }
                if choice := self.view.input_menu(menu):
                    round_table[selected_match - 1]["Winner"] = choice
                    rounds.results[selected_match - 1] = True

        rounds.end_round = datetime.now().strftime("%d/%m/%Y %H:%M")
        round_title += f" | End: {rounds.end_round}"
        round_title = "Results of " + round_title

        self.update_scores(rounds, round_table)
        round_table = rounds.get_matches_table(matches)
        for line in round_table:
            for key in ["key", "", "Winner"]:
                del line[key]
        self.actual_tournament.rounds.append({
            f"Round {round_number}": {
                "Started at:": rounds.start_round,
                "Ended at:": rounds.end_round,
                "Matches": round_table
            }
        })
        self.tournament_db.save(self.actual_tournament)
        self.view.view_table(round_title, round_table)
        self.view.simple_input(f"Press enter to continue")
        rounds.start_round, rounds.end_round = "", ""

    def start_tournament(self):
        if not self.actual_tournament.start[0]:
            if len(self.actual_tournament.players) % 2 == 0:
                self.actual_tournament.start = (True, datetime.now().strftime("%d-%m-%Y %H:%M"))
                self.tournament_db.save(self.actual_tournament)
                players = random.sample(self.actual_tournament.players, len(self.actual_tournament.players))
                rounds = Rounds(players)

                for i in range(1, self.actual_tournament.number_of_round + 1):
                    self.start_round(rounds, i)

                self.actual_tournament.end = (True, datetime.now().strftime("%d-%m-%Y %H:%M"))
                if self.view.confirm("Do you add a comment for this tournament ?"):
                    self.add_tournament_comment()
            else:
                self.view.view_message("Number of player is impair !")
                if self.view.confirm("Do you add a new player ?"):
                    self.add_tournament_player()
        else:
            self.view.view_error_message("Tournament is already started !")

    def tournament_header(self) -> None:
        data = [{
            "Tournament name": self.actual_tournament.name,
            "Place": self.actual_tournament.place,
            "Start date": self.actual_tournament.start[1] if self.actual_tournament.start[0] else "No started !",
            "End date": self.actual_tournament.end[1] if self.actual_tournament.end[0] else "No finished !"
        }]
        self.view.view_table("tournament", data)

    def get_tournament_players(self) -> None:
        players = [player.__dict__ for player in self.actual_tournament.players]
        players.sort(key=lambda player: player.get("lastname"))
        self.view.view_table("Players in tournament", players)

    def add_tournament_comment(self) -> None:
        if self.actual_tournament.comment:
            if not self.view.confirm("Comment already exist, do you create new comment ?"):
                return None
        comment = self.view.simple_input("Enter your comment (enter to valid): ")
        self.actual_tournament.comment = comment
        self.tournament_db.save(self.actual_tournament)

    def rounds_and_matches(self):
        loop = True
        while loop:
            round_selection = {}
            for key, round in enumerate(self.actual_tournament.rounds):
                round_selection[str(key + 1)] = list(round.keys())[0]
            back = str(len(self.actual_tournament.rounds) + 1)
            round_selection[back] = "Back"
            choice = self.view.input_menu(round_selection)
            if choice == str(back):
                loop = False
            else:
                round = self.actual_tournament.rounds[int(choice) - 1].get(f"Round {choice}")
                self.view.view_table(f"Round {choice}", round.get("Matches"))
