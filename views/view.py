from rich.console import Console
from rich.table import Table
from rich import print, box

CYAN = "bold dark_cyan"
ORANGE = "bold bold dark_orange3"
BLUE = "bold dodger_blue2"
GREEN = "bold green3"
RED = "bold red"


class View:
    def __init__(self) -> None:
        self.console = Console()

    def view_table(self, title: str, data: list[dict]) -> None:
        self.console.clear()
        if data:
            table = Table(title=title, min_width=80, style=BLUE, box=box.ROUNDED)
            table.header_style = BLUE
            table.row_styles = ["dim", ""]
            for column in data[0].keys():
                table.add_column(column)
            for player in data:
                table.add_row(*list(player.values()))
            self.console.print(table)
        else:
            self.view_error_message("No data !")
        self.simple_input("Press enter to continue")

    def view_message(self, description: str) -> None:
        self.console.print(description, style=GREEN)

    def view_error_message(self, description: str) -> None:
        self.console.print(description, style=RED)

    def input_menu(self, menu_list: list | None) -> str | None:
        self.console.clear()
        run = True
        while run:
            keys = [menu[0] for menu in menu_list]
            table = Table(box=box.ROUNDED, min_width=80, style=CYAN, header_style=CYAN, show_lines=True, show_header=False)
            table.add_column("Key", justify="center")
            table.add_column("Menu", justify="center", max_width=10)
            for menu in menu_list:
                table.add_row(*menu, style=CYAN)
            print(table)
            choice = self.console.input(f"[{ORANGE}]Your key choice: [/]")
            if choice in keys:
                return choice
            else:
                self.view_error_message('Invalid input !')
                return None

    def user_input(self, fields: dict) -> dict:
        inputs = {}
        for key, value in fields.items():
            inputs[key] = self.console.input(f"[{ORANGE}]{value}[/]")
        return inputs

    def confirm(self, message: str) -> bool:
        choice = self.console.input(f"[{ORANGE}]{message} Y/n [/]? ")
        if choice == "Y" or choice == "y":
            return True
        return False

    def simple_input(self, message) -> str:
        choice = self.console.input(f"[{ORANGE}]{message}")
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
