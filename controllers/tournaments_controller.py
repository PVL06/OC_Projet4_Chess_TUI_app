from datetime import datetime
import random


from views.view import View
from models.tournaments_model import Tournament, TournamentsDb, Round
from models.players_model import PlayersDb


class TournamentCtl:
    def __init__(self) -> None:
        self.actual_tournament = None
        self.actual_round = []
        self.round_result = []
        self.view = View()
        self.players_db = PlayersDb()
        self.tournament_db = TournamentsDb()

    def create_new_tournament(self) -> None:
        tournaments_name = [tournament.name for tournament in self.tournament_db.get_all_tournaments()]
        run = True
        while run:
            user_input = self.view.create_tournament()
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
                            "end": (False, "")
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

    def add_tournament_player(self) -> None: # todo: ajouter fonction pour dire si assez de joueur par rapport au nombre de round
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

    # todo: verifier l'entrée dans selected_match, numeric et dans l'interval du nombre de match
    def enter_round_result(self, matches_data: list) -> dict:
        self.view.view_table(self.actual_round.round_name, matches_data)
        selected_match = int(self.view.simple_input("enter match number: "))
        menu = {
            "1": "player 1 win",
            "2": "player 2 win",
            "3": "draw"
        }
        if choice := self.view.input_menu(menu):
            matches_data[int(selected_match)]["Winner"] = choice
            self.round_result[selected_match] = True
            return matches_data

    def start_round(self, round_number):
        # Create a round and add match
        if round_number == 1:
            players = random.sample(self.actual_tournament.players, len(self.actual_tournament.players))
            players_match = [[player.short_player(), 0] for player in players]
        else:
            players_match = []
            for player1, player2 in self.actual_round.matches:
                players_match.append(player1)
                players_match.append(player2)
            players_match.sort(key=lambda player: player[1])
            self.round_result = []

        self.actual_round = Round(f"Round {round_number}", start="", end="", matches=[])
        for i in range(0, len(players_match), 2):
            match = (players_match[i], players_match[i+1])
            self.actual_round.matches.append(match)
            self.round_result.append(False)

        # show and select stop round or match result
        matches_data = []
        for index, match in enumerate(self.actual_round.matches):
            matches_data.append({
                "match key": str(index),
                "player 1 (WHITE)": match[0][0],
                "score 1": str(match[0][1]),
                "": "vs",
                "player 2 (BLACK)": match[1][0],
                "score 2": str(match[1][1]),
                "Winner": ""
            })

        self.view.view_table(f"Round {round_number}", matches_data)
        self.view.enter_input(f"Press enter to start the round {round_number} ")
        self.actual_round.start = datetime.now().strftime("%d/%m/%Y %H:%M")
        loop = True
        while loop:
            self.view.view_table(self.actual_round.round_name, matches_data)
            if not self.actual_round.end:
                menu = {
                    "1": "Enter match result",
                    "2": "Stop round"
                }
                choice = self.view.input_menu(menu)
                if choice == "1":
                    self.enter_round_result(matches_data)
                elif choice == "2":
                    self.actual_round.end = datetime.now().strftime("%d/%m/%Y %H:%M")
            else:
                if not all(self.round_result):
                    self.enter_round_result(matches_data)
                else:
                    results = [int(result.get("Winner")) for result in matches_data]
                    for index, result in enumerate(results):
                        if result == 1:
                            self.actual_round.matches[index][0][1] += 1
                        elif result == 2:
                            self.actual_round.matches[index][1][1] += 1
                        else:
                            self.actual_round.matches[index][0][1] += 0.5
                            self.actual_round.matches[index][1][1] += 0.5
                    #self.actual_tournament.rounds.append(self.actual_round)
                    round = self.actual_round.__dict__.copy()
                    self.actual_tournament.rounds.append(round)
                    self.tournament_db.save(self.actual_tournament)
                    loop = False

    def start_tournament(self): # todo: a finir avec date et heure de fin de tournoi et commentaire
        if not self.actual_tournament.end[0]:
            self.actual_tournament.start = (True, datetime.now().strftime("%d-%m-%Y %H:%M"))
            self.tournament_db.save(self.actual_tournament)

            for i in range(1, self.actual_tournament.number_of_round + 1):
                self.start_round(i)

    def tournament_header(self) -> None:
        data = [{
            "Tournament name": self.actual_tournament.name,
            "Place": self.actual_tournament.place,
            "Start date": self.actual_tournament.start[1] if self.actual_tournament.start[0] else "No started !",
            "End date": self.actual_tournament.end[1] if self.actual_tournament.end[0] else "No started !"
        }]
        self.view.view_table("tournament", data)

    def get_tournament_players(self) -> None:
        players = [player.__dict__ for player in self.actual_tournament.players]
        players.sort(key=lambda player: player.get("lastname"))
        self.view.view_table("Players in tournament", players)

    def rounds_and_matches(self):
        pass
