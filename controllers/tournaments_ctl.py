import copy
from datetime import datetime
import random
import itertools

from models.players_model import PlayersDb
from views.view import View
from models.tournaments_model import Tournament, TournamentsDb, Round
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
                    "status": self.utils.tournament_status(tournament)
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


class ActualTournament:
    def __init__(self):
        self.actual_tournament = None
        self.round_result = []
        self.view = View()
        self.players_db = PlayersDb()
        self.tournament_db = TournamentsDb()
        self.utils = Utils()

    def add_tournament_player(self) -> None:
        players_id_db = [player.id for player in self.players_db.get_all_players()]
        loop = True
        while loop:
            players_tournament_id = [player[0] for player in self.actual_tournament.players]
            players_available = [player_id for player_id in players_id_db if player_id not in players_tournament_id]
            if players_available:
                if not self.actual_tournament.start:
                    players = [self.players_db.get_player(id) for id in players_available]
                    if player := self.utils.players_selection(players):
                        self.actual_tournament.players.append([player.id, 0])
                        self.tournament_db.save(self.actual_tournament)
                        messages = [
                            f"Player: '{player.__str__()}' added !",
                            f"players in this tournament: {len(self.actual_tournament.players)}",
                        ]
                        if len(self.actual_tournament.players) % 2 == 1:
                            messages.append("You need to add player for pairing players !")
                        self.view.view_message("\n".join(messages), continue_enter=False)

                    if not self.view.confirm("add new player ?"):
                        loop = False
                else:
                    self.view.view_message("Don't add player in started tournament !", error=True)
                    loop = False
            else:
                self.view.view_message("All players in tournament or no players in register !", error=True)
                loop = False

    def remove_tournament_player(self) -> None:
        if not self.actual_tournament.start:
            players = [self.players_db.get_player(player[0]) for player in self.actual_tournament.players]
            player = self.utils.players_selection(players)
            for i in range(len(players)):
                if player.id == players[i].id:
                    if self.view.confirm(f"Sure to remove player: {player.__str__()}"):
                        del self.actual_tournament.players[i]
                        self.tournament_db.save(self.actual_tournament)
                        self.view.view_message(f"Player removed: {player.__str__()}")
                    break
        else:
            self.view.view_message("Don't remove player in started tournament !", error=True)

    def start_tournament(self) -> None:
        tournament = self.actual_tournament
        if not tournament.end:
            if len(tournament.players) % 2 == 0 and len(tournament.players) >= 4:
                tournament.start = datetime.now().strftime("%d-%m-%Y %H:%M")

                if not tournament.combination:
                    players_id = [player[0] for player in tournament.players]
                    tournament.combination = list(itertools.combinations(players_id, 2))
                    tournament.combination = random.sample(tournament.combination, len(tournament.combination))
                self.tournament_db.save(tournament)

                round_number = len(tournament.rounds) + 1
                if round_number <= tournament.number_of_round:
                    for i in range(round_number, tournament.number_of_round + 1):
                        self._start_round(i)

                self.actual_tournament.end = datetime.now().strftime("%d-%m-%Y %H:%M")
                self.tournament_db.save(self.actual_tournament)
                if self.view.confirm("Do you add a comment for this tournament ?"):
                    self.add_tournament_comment()
            else:
                self.view.view_message("Number of player is impair !", error=True)
        else:
            self.view.view_message("Tournament is finished !", error=True)

    def view_tournament_header(self) -> None:
        data = [{
            "Tournament name": self.actual_tournament.name,
            "Place": self.actual_tournament.place,
            "Number of round": str(self.actual_tournament.number_of_round),
            "Status": self.utils.tournament_status(self.actual_tournament)
        }]
        self.view.table_view("Tournament header", data)
        self.view.enter_continue()

    def view_tournament_players(self) -> None:
        players = [self.players_db.get_player(player[0]).__dict__ for player in self.actual_tournament.players]
        players.sort(key=lambda player: player.get("lastname"))
        self.view.table_view("Players in tournament", players)
        self.view.enter_continue()

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
            menu = []
            for i in range(len(self.actual_tournament.rounds)):
                menu.append((str(i+1), self.actual_tournament.rounds[i].get("name")))
            back_selection = [("0", "Back")]
            choice = self.view.input_menu(back_selection + menu)
            if choice:
                if choice == "0":
                    loop = False
                else:
                    choice = self.utils.check_input_number(choice, len(self.actual_tournament.rounds))
                    selected_round = self.actual_tournament.rounds[choice - 1]
                    print(selected_round.get("matches")[0])
                    self.view.table_view(selected_round.get("name"), selected_round.get("matches")[0])
                    self.view.enter_continue()

    def _start_round(self, round_number: int) -> None:
        round = Round(round_number)
        combination = self.actual_tournament.combination
        combination.sort(key=lambda player_id: abs(self._get_score(player_id[0]) - self._get_score(player_id[1])))

        matches = self._get_matches()
        round_title = f"{round.name}/{self.actual_tournament.number_of_round}"
        round_table = self._get_matches_table(matches)
        self.round_result = [False] * len(matches)
        self.view.table_view(round_title, round_table)
        self.view.simple_input(f"Press enter to start {round_title}")
        round.round_start = datetime.now().strftime("%d-%m-%Y %H:%M")
        round_title += f"  Start: {round.round_start}"

        while not all(self.round_result):
            self.view.table_view(round_title, round_table)
            selected_match = self.view.simple_input("Enter match number: ")
            selected_match = self.utils.check_input_number(selected_match, len(matches))
            if not selected_match:
                self.view.view_message("Selection out of range", error=True)
                continue
            choice_menu = "Enter match result (0: draw, 1: player1 win, 2: player 2 win): "
            choice_result = self.view.simple_input(choice_menu)
            if selected_match and choice_result in ["0", "1", "2"]:
                round_table[selected_match - 1]["Winner"] = str(choice_result)
                self.round_result[selected_match - 1] = True
            else:
                self.view.view_message("Bad input for result selection !")

        round.round_stop = datetime.now().strftime("%d/%m/%Y %H:%M")
        round_title += f" | End: {round.round_stop}"
        round_title = "Results of " + round_title

        self._update_scores(round_table)
        updated_matches = self._update_matches(matches)
        round.matches.append(copy.deepcopy(updated_matches))
        round_table = self._get_matches_table(matches)
        for line in round_table:
            for key in ["key", "", "Winner"]:
                del line[key]
        self.view.table_view(round_title, round_table)
        self.actual_tournament.rounds.append(round.__dict__)
        self.tournament_db.save(self.actual_tournament)
        self.view.enter_continue()

    def _get_matches(self):
        players_id = [player[0] for player in self.actual_tournament.players]

        matches = []
        for combination in self.actual_tournament.combination:
            if combination[0] in players_id and combination[1] in players_id:
                players_id.remove(combination[0])
                players_id.remove(combination[1])
                player_1 = self._get_player_score(combination[0])
                player_2 = self._get_player_score(combination[1])
                matches.append((player_1, player_2))
                self.actual_tournament.combination.remove(combination)

        if players_id:
            for i in range(0, len(players_id), 2):
                player_1 = self._get_player_score(players_id[i])
                player_2 = self._get_player_score(players_id[i+1])
                matches.append((player_1, player_2))

        return matches

    def _get_score(self, player_id: str) -> int:
        for player in self.actual_tournament.players:
            if player[0] == player_id:
                return player[1]

    def _get_player_score(self, player_id: str) -> int:
        for player in self.actual_tournament.players:
            if player[0] == player_id:
                return player

    def _get_matches_table(self, matches) -> list[dict]:
        matches_table = []
        for index, match in enumerate(matches):
            table_row = {
                "key": str(index + 1),
                "player 1 (WHITE)": self.players_db.get_player(match[0][0]).__str__(),
                "player 1 score": str(match[0][1]),
                "": "VS",
                "player 2 (BLACK)": self.players_db.get_player(match[1][0]).__str__(),
                "player 2 score": str(match[1][1]),
                "Winner": ""
            }
            matches_table.append(table_row)
        return matches_table

    def _update_scores(self, round_table) -> None:
        for line in round_table:
            match line.get("Winner"):
                case "0":
                    self._add_player_point(line.get("player 1 (WHITE)").split(" ")[0], 0.5)
                    self._add_player_point(line.get("player 2 (BLACK)").split(" ")[0], 0.5)
                case "1":
                    self._add_player_point(line.get("player 1 (WHITE)").split(" ")[0], 1)
                case "2":
                    self._add_player_point(line.get("player 2 (BLACK)").split(" ")[0], 1)

    def _update_matches(self, matches):
        updated_match = []
        for match in matches:
            player_1 = self._get_player_score(match[0][0])
            player_2 = self._get_player_score(match[1][0])
            updated_match.append((player_1, player_2))
        return updated_match

    def _add_player_point(self, player_id: str, point: float) -> None:
        print(player_id)
        for i in range(len(self.actual_tournament.players)):
            if player_id == self.actual_tournament.players[i][0]:
                self.actual_tournament.players[i][1] += point
                break
