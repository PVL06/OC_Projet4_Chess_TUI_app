from rich.console import Console
from rich.table import Table


class View:
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

    def check_select_input(self, message: str, selection: list[int]) -> int | None:
        choice = input(message)
        try:
            choice = int(choice)
        except ValueError:
            self.view_error_message("Enter a number !")
        else:
            if choice in selection:
                return choice
            self.view_error_message("Number not in selection !")
        return None
