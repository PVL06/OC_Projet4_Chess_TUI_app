from rich.console import Console
from rich.table import Table


class Viewer:
    def __init__(self) -> None:
        self.console = Console()

    def view_table(self, data: list[dict], title: str):
        if data:
            table = Table(title=title, style="blue")
            table.header_style = "bold blue"
            table.row_styles = ["dim", ""]
            for column in data[0].keys(): table.add_column(column)
            for player in data: table.add_row(*list(player.values()))
            self.console.print(table)
        else:
            self.view_error_message("No data !!!")

    def view_message(self, description: str):
        self.console.print(description, style="green")

    def view_error_message(self, description: str):
        self.console.print(description, style="red")

    def input_menu(self, menu: dict):
        run = True
        while run:
            for key, value in menu.items():
                print(key,"->" ,value)
            choice = input("Your choice: ")
            if choice in menu.keys():
                run = False
                return choice
            
    def user_input(self, fields: dict):
        inputs = {}
        for key, value in fields.items():
            inputs[key] = input(value)
        return inputs
    
    def confirm(self, message: str) -> bool:
        choice = input(f"{message} Y/n ? ")
        if choice == "Y" or choice == "y":
            return True
        return False


