from rich.console import Console
from rich.table import Table
from rich import print, box

CYAN = "dark_cyan"
ORANGE = "bold dark_orange3"
GREEN = "bold green3"
RED = "bold red"


class View:
    """
    Class with functions to show different output or input for user interface
    """

    def __init__(self) -> None:
        self.console = Console()

    def table_view(self, title: str, data: list[dict], selection=False) -> bool:
        """
        Display a table with rich table
        :param title: the table title
        :param data: list of dict, each dict in list represent one line in table
        :param selection: (default=False), if True add one column in first place with number in range 1 to n
        :return: True if data not empty else return False
        """
        self.console.clear()
        if data:
            table = Table(title=title, min_width=80, style=CYAN, box=box.ROUNDED)
            table.header_style = "bold CYAN"
            table.row_styles = ["bold dim", "bold CYAN"]
            if selection:
                table.add_column("key")
            for column in data[0].keys():
                table.add_column(column)
            for key, item in enumerate(data):
                list_values = list(item.values())
                if selection:
                    list_values.insert(0, str(key + 1))
                table.add_row(*list_values)
            self.console.print(table)
            return True

    def view_message(self, description: str, error=False, continue_enter=True) -> None:
        """ Show message 'description'"""
        self.console.print(description, style=RED if error else GREEN)
        if continue_enter:
            self.enter_continue()

    def enter_continue(self):
        """Prompt for continue"""
        self.console.input(f"[{ORANGE}]Press enter to continue[/]")

    def input_menu(self, menu_list: list | None) -> str | None:
        """
        Display table with rich and asks the user for their choice
        :param menu_list: List of tuples containing a choice and a prompt
        :return: user choice
        """
        self.console.clear()
        table = Table(box=box.ROUNDED,
                      min_width=80,
                      style=CYAN,
                      header_style="bold CYAN",
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
        """
        Displays a list of prompts
        :param fields: dict with key and prompt
        :return: Returns a dictionary with the same input keys and the values entered by the user
        """
        inputs = {}
        for key, value in fields.items():
            inputs[key] = self.console.input(f"[{ORANGE}]{value}[/]")
        return inputs

    def confirm(self, message: str) -> bool:
        """
        Display message with prompt for confirm
        :param message: message to display
        :return: True if the user choice y or Y else False
        """
        choice = self.console.input(f"[{ORANGE}]{message} Y/n [/]? ")
        if choice == "Y" or choice == "y":
            return True
        return False

    def simple_input(self, message) -> str:
        """Display simple input with message and return user input"""
        choice = self.console.input(f"[{ORANGE}]{message}")
        return choice
