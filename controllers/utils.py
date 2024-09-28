from views.view import View
from controllers.players_ctl import Player
from models.tournaments_model import Tournament


class Utils:
    def __init__(self):
        self.view = View()

    def players_selection(self, players: list[Player]) -> Player | None:
        """
        Show table of players and a user input to select player
        return selected player object
        """

        players_dict = [player.__dict__ for player in players]
        self.view.table_view("Select player", players_dict, selection=True)
        choice = self.view.simple_input("Enter key value: ")
        try:
            choice = int(choice) - 1
        except ValueError:
            self.view.view_message("Invalid input !", error=True)
        else:
            if 0 <= choice < len(players):
                return players[choice]
            else:
                self.view.view_message("Input out of range !", error=True)

    @staticmethod
    def check_input_number(choice: str, max_value: int) -> int | None:
        """Check value of user input if is a number and return user input int"""

        try:
            choice = int(choice)
        except ValueError:
            return None
        else:
            if 1 <= choice <= max_value:
                return choice

    @staticmethod
    def tournament_status(tournament: Tournament) -> str:
        """Check status of tournament and return status string"""

        if tournament.start and tournament.end:
            return f"Finished it {tournament.end}"
        elif tournament.start and not tournament.end:
            return f"Started it {tournament.start} but no finished"
        else:
            return "No started"
