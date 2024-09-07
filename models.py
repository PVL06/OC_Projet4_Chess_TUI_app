import os
import json
import random
import datetime

from pydantic import BaseModel, Field


class Player(BaseModel):
    id: str = Field(pattern=r"^([A-Z]{2})([0-9]{5})$")
    firstname: str = Field(pattern=r"^[a-zA-Z -]*$", min_length=2)
    lastname: str = Field(pattern=r"^[a-zA-Z -]*$", min_length=2)
    date_of_birth: str = Field(pattern=r"^(0[1-9]|[12][0-9]|3[01])\/(0[0-9]|1[012])\/([0-9]{4})$")

    def __str__(self) -> str:
        return f"{self.id} {self.firstname} {self.lastname}"
    

class PlayersRegister:
    def __init__(self) -> None:
        self.players_file_path = "data/players.json"
        if not os.path.exists("data/"):
            os.mkdir("data")

    def save_player(self, player: Player) -> bool:
        if player.id not in [player.id for player in self.get_players()]:
            if os.path.exists(self.players_file_path):
                with open(self.players_file_path, "r+") as file:
                    data = json.load(file)
                    data["players"].append(player.__dict__)
                    file.seek(0)
                    json.dump(data, file, indent=4)
            else:
                with open(self.players_file_path, "w") as file:
                    json.dump({'players': [player.__dict__]}, file, indent=4)
            return True
        return False

    def get_players(self) -> list[Player] | None:
        if os.path.exists(self.players_file_path):
            with open(self.players_file_path, "r") as file:
                data = json.load(file)
                return [Player(**player) for player in data["players"]]
        return None


class Tournament:
    # todo: sauvegarder a chaque modification
    def __init__(self, name: str, place: str, number_of_round=4) -> None:
        self.name = name
        self.place = place
        self.players = []
        self.number_of_round = number_of_round
        self.start = (False, "")
        self.end = (False, "")
        self.actual_turn = 0

    # todo: verifier si joueur pas deja dans la liste
    def add_player(self, player: Player) -> bool:
        if not self.start[0]:
            self.players.append([player, 0])
            return True
        return False

    def start_tournament(self) -> bool:
        if not self.start[0] and len(self.players)%2 == 0:
            date = datetime.datetime.now()
            self.start = (True, date.strftime("%d/%m/%Y %X"))
            random.shuffle(self.players)
            return True
        return False
    
    def start_new_round(self):
        self.actual_turn += 1
        if self.actual_turn < self.number_of_round:
            round = Round(self.players, self.actual_turn)
            return round.create_round()
            #todo: return round player pair


    def end_tournament(self):
        date = datetime.datetime.now()
        self.end = (True, date.strftime("%d/%m/%Y %X"))

    def add_description(self, description):
        pass

    def save_tournament(self):
        pass

class Round:
    def __init__(self, players, turn_number) -> None:
        self.players = players
        self.round_number = turn_number
        self.player_pair = []

    def create_round(self):
        if self.round_number == 1:
            for i in range(0, len(self.players), 2):
                match = Match(self.players[i], self.players[i+1])
                self.player_pair.append(match) 
        else:
            pass

        return self.player_pair


class Match:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2
        self.match = ([player1, 0], [player2, 0])

    def color_player(self):
        color = ["white", "black"]
        random.shuffle(color)
        return (self.player1, color[0], self.player2, color[1])

if __name__ == "__main__": # test
    register = PlayersRegister()
    tournament = Tournament('test', 'avignon')

    players = register.get_players()
    tournament.add_player(players[0])
    tournament.add_player(players[1])
    tournament.add_player(players[2])
    tournament.add_player(players[3])
    tournament.add_player(players[4])
    tournament.add_player(players[5])

    tournament.start_tournament()

    print(tournament.start_new_round())