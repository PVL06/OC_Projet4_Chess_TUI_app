from datetime import datetime
import random
import itertools

from models.players_model import PlayersDb, Player
from views.view import View
from models.tournaments_model import Tournament, TournamentsDb
from controllers.utils import Utils


class TournamentsCtl:
    def __init__(self) -> None:
        self.view = View()
        self.tournament_db = TournamentsDb()
        self.actual_tournament = ActualTournament()
        self.utils = Utils()

    def create_new_tournament(self) -> None:
        tournaments_name = [tournament.name for tournament in self.tournament_db.get_all_tournaments()]
        fields = {
            "name": "Tournament name: ",
            "place": "Tournament place: ",
            "number_of_round": "Number of round (4 round if no value): "
        }
        user_input = self.view.multiple_inputs(fields)

        if user_input.get("name") not in tournaments_name:
            rounds_number = user_input.get("number_of_round")
            try:
                rounds_number = int(rounds_number) if rounds_number else 4
            except ValueError:
                self.view.view_message("Round must be an integer in range 4 to 10 !", error=True)
            else:
                if 4 <= rounds_number <= 10:
                    tournament = Tournament(user_input.get("name"), user_input.get("place"), rounds_number)
                    self.tournament_db.save(tournament)
                    self.view.view_message(f"New tournament '{user_input.get('name')}' created !")
                else:
                    self.view.view_message("Round must be in range 4 to 10 !", error=True)
        else:
            self.view.view_message(f"Tournament: '{user_input.get('name')}' already exist !", error=True)

    def select_tournament(self) -> Tournament | None:
        if tournaments := self.tournament_db.get_all_tournaments():
            data = []
            for tournament in tournaments:
                data.append({
                    "Tournament name": tournament.name,
                    "Place": tournament.place,
                    "Number of round": str(tournament.number_of_round),
                    "Started": tournament.start if tournament.start else "No started",
                    "Ended": tournament.end if tournament.end else "No finished"
                })
            self.view.table_view("Select tournament", data, selection=True)
            choice = self.view.simple_input("Enter key tournament: ")
            if choice := self.utils.check_input_number(choice, len(tournaments)):
                tournament = tournaments[choice - 1]
                self.view.view_message(f"Tournament '{tournament.name}' selected")
                return tournament
            else:
                self.view.view_message("Invalid input !", error=True)
        else:
            self.view.view_message("No tournament !", error=True)

    def all_tournaments(self) -> None:
        tournaments = self.tournament_db.get_all_tournaments()
        data = []
        for tournament in tournaments:
            data.append({
                "Tournament name": tournament.name,
                "Place": tournament.place,
                "Number of round": str(tournament.number_of_round),
                "Status": self.utils.tournament_status(tournament)
            })
        self.view.table_view("Select tournament", data)
        self.view.enter_continue()


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
                player2 = self.get_player_score(players_id[i + 1])
                if player1 and player2:
                    matches.append((player1, player2))

        return matches

    @staticmethod
    def get_matches_table(matches) -> list[dict]:
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


class ActualTournament:
    def __init__(self):
        self.actual_tournament = None
        self.view = View()
        self.players_db = PlayersDb()
        self.tournament_db = TournamentsDb()
        self.utils = Utils()

    def add_tournament_player(self) -> None:
        players_db = self.players_db.get_all_players()
        loop = True
        while loop:
            players_tournament_id = [player.id for player in self.actual_tournament.players]
            players_available = [player for player in players_db if player.id not in players_tournament_id]
            if players_available:
                if not self.actual_tournament.start:
                    if player := self.utils.players_selection(players_available):
                        self.actual_tournament.players.append(player)
                        self.tournament_db.save(self.actual_tournament)
                        messages = [
                            f"Player: '{player.__str__()}' added !",
                            f"players in this tournament: {len(self.actual_tournament.players)}",
                        ]
                        if len(self.actual_tournament.players) % 2 == 1:
                            messages.append("You need to add player for pairing players !")
                        self.view.view_message("\n".join(messages))

                    if not self.view.confirm("add new player ?"):
                        loop = False
                else:
                    self.view.view_message("Don't add player in started tournament !", error=True)
                    loop = False
            else:
                self.view.view_message("All players in tournament or no players in register !", error=True)
                loop = False

    def remove_tournament_player(self) -> None:
        player = self.utils.players_selection(self.actual_tournament.players)
        for i in range(len(self.actual_tournament.players)):
            if player.id == self.actual_tournament.players[i].id:
                if self.view.confirm(f"Sure to remove player: {player.__str__()}"):
                    del self.actual_tournament.players[i]
                    self.tournament_db.save(self.actual_tournament)
                    self.view.view_message(f"Player removed: {player.__str__()}")
                break

    def start_tournament(self) -> None:
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

    def start_round(self, rounds: Rounds, round_number: int) -> None:
        round_title = f"Round {round_number}/{self.actual_tournament.number_of_round}"
        matches = rounds.get_matches()
        round_table = rounds.get_matches_table(matches)
        rounds.results = [False] * len(matches)

        self.view.view_table(round_title, round_table)
        self.view.simple_input(f"Start round {round_number} (press enter) ?")
        rounds.start_round = datetime.now().strftime("%d-%m-%Y %H:%M")
        round_title += f"  Start: {rounds.start_round}"

        selection = [i + 1 for i in range(len(matches))]
        while not all(rounds.results):
            self.view.view_table(round_title, round_table)
            selected_match = self.view.check_select_input("Enter match number: ", selection)
            choice_menu = "Enter match result (0: draw, 1: player1 win, 2: player 2 win): "
            choice_result = self.view.check_select_input(choice_menu, [0, 1, 2])
            if selected_match and choice_result in [0, 1, 2]:
                round_table[selected_match - 1]["Winner"] = str(choice_result)
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

    def tournament_header(self) -> None:
        data = [{
            "Tournament name": self.actual_tournament.name,
            "Place": self.actual_tournament.place,
            "Number of round": str(self.actual_tournament.number_of_round),
            "Status": self._tournament_status(self.actual_tournament)
        }]
        self.view.table_view("Tournament header", data)
        self.view.enter_continue()

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

    def rounds_and_matches(self) -> None:
        loop = True
        while loop:
            keys = []
            for round in self.actual_tournament.rounds:
                keys.append(list(round.keys())[0])
            round_selection = [("0", "Back")]
            for i in range(len(self.actual_tournament.rounds)):
                round_selection.append((str(i + 1), keys[i]))
            choice = self.view.input_menu(round_selection)
            if choice:
                if choice == "0":
                    loop = False
                else:
                    round_name = f"Round {str(int(choice))}"
                    selected_round = self.actual_tournament.rounds[int(choice) - 1][round_name]["Matches"]
                    self.view.view_table(f"Round {round_name}", selected_round)

    @staticmethod
    def _check_input_number(choice: str, max_value: int) -> int | None:
        try:
            choice = int(choice)
        except ValueError:
            pass
        else:
            if 1 <= choice <= max_value:
                return choice

    @staticmethod
    def _tournament_status(tournament: Tournament) -> str:
        if tournament.start and tournament.end:
            return f"Finished it {tournament.end}"
        elif tournament.start and not tournament.end:
            return f"Started it {tournament.start} but no finished"
        else:
            return "No started"

