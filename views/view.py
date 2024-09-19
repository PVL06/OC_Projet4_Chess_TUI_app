from rich.console import Console
from rich.table import Table


class Viewer:
    def __init__(self) -> None:
        self.console = Console()

    def view_table(self, title: str, data: list[dict]):
        if data:
            table = Table(title=title, style="blue")
            table.header_style = "bold blue"
            table.row_styles = ["dim", ""]
            for column in data[0].keys():
                table.add_column(column)
            for player in data:
                table.add_row(*list(player.values()))
            self.console.clear()
            self.console.print(table)
        else:
            self.view_error_message("No data !")

    def view_message(self, description: str):
        self.console.print(description, style="green")

    def view_error_message(self, description: str):
        self.console.print(description, style="red")

    def input_menu(self, menu: dict | None):
        run = True
        while run:
            for key, value in menu.items():
                print(key, "->", value)
            choice = input("Your choice: ")
            print("*"*30)
            if choice in menu.keys():
                return choice
            else:
                self.view_error_message('Invalid input !')
                return None

    @staticmethod
    def user_input(fields: dict):
        inputs = {}
        for key, value in fields.items():
            inputs[key] = input(value)
        print("*" * 30)
        return inputs

    @staticmethod
    def confirm(message: str) -> bool:
        choice = input(f"{message} Y/n ? ")
        print("*" * 30)
        if choice == "Y" or choice == "y":
            return True
        return False

    @staticmethod
    def simple_input(message):
        choice = input(message)
        return choice

    @staticmethod
    def enter_input(message):
        input(message)


class View(Viewer):
    def __init__(self) -> None:
        super().__init__()

    def main_menu(self):
        menu = {
            "1": "Players",
            "2": "Tournaments",
            "3": "Quit"
        }
        return self.input_menu(menu)

    def players_menu(self):
        menu = {
            "1": "Add new player to register",
            "2": "View players register",
            "3": "Back"
        }
        return self.input_menu(menu)

    def tournaments_menu(self):
        menu = {
            "1": "Create new tournament",
            "2": "Select tournament",
            "3": "View all tournaments",
            "4": "Back"
        }
        return self.input_menu(menu)

    def tournament_menu(self):
        menu = {
            "1": "Start tournament",
            "2": "Add player to tournament",
            "3": "View tournament name, place and date",
            "4": "Tournament players",
            "5": "View rounds and matchs",
            "6": "Back"
        }
        return self.input_menu(menu)

    def new_player(self):
        fields = {
            "id": "Player id (ex: DF12345): ",
            "firstname": "Firstname: ",
            "lastname": "Lastname: ",
            "date_of_birth": "Date of birth (dd/mm/yyyy): "
            }
        return self.user_input(fields)

    def create_tournament(self):
        fields = {
            "name": "Tournament name: ",
            "place": "Tournament place: ",
            "number_of_round": "Nombre de tour (4 round si sans valeur): "
        }
        return self.user_input(fields)
