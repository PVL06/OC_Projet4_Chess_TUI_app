from rich.console import Console
from rich.table import Table
from rich import print, box

CYAN = "dark_cyan"
ORANGE = "bold dark_orange3"
BLUE = "dodger_blue2"
GREEN = "bold green3"
RED = "bold red"


class View:
    def __init__(self) -> None:
        self.console = Console()

    def table_view(self, title: str, data: list[dict], selection=False) -> bool:
        self.console.clear()
        if data:
            table = Table(title=title, min_width=80, style=CYAN, box=box.ROUNDED)
            table.header_style = f"bold CYAN"
            table.row_styles = ["bold dim", "bold CYAN"]
            for column in data[0].keys():
                table.add_column(column)
            for key, item in enumerate(data):
                list_values = list(item.values())
                if selection:
                    list_values.insert(0, str(key))
                table.add_row(*list_values)
            self.console.print(table)
            return True

    def view_message(self, description: str, error=False) -> None:
        self.console.print(description, style=RED if error else GREEN)
        self.enter_continue()

    def enter_continue(self):
        self.console.input(f"[{ORANGE}]Press on key to continue[/]")

    def input_menu(self, menu_list: list | None) -> str | None:
        self.console.clear()
        table = Table(box=box.ROUNDED,
                      min_width=80,
                      style=CYAN,
                      header_style=f"bold CYAN",
                      show_lines=True,
                      show_header=False)
        table.add_column("Key", justify="center")
        table.add_column("Menu", justify="center", max_width=10)
        for menu in menu_list:
            table.add_row(*menu, style=f"bold {CYAN}")
        print(table)
        choice = self.console.input(f"[{ORANGE}]Your key choice: [/]")
        return choice

    def multiple_inputs(self, fields: dict) -> dict:
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
