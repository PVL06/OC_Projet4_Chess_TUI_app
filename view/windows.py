import msvcrt
from rich.live import Live
from rich.layout import Layout

from box import SelectBox, InputBox


MAIN_MENU = ["Players", "Tournament", "Quit"]
PLAYERS_MENU = ["Add player", "Players register", "Back"]
TOURNAMENT_MENU = ["New tournament", "Tournaments register", "Back"]
PLAYER_INPUT = [
    "Identifiant national d'échec (format exemple: AB12345) :",
    "Prénom du joueur :",
    "Nom de famille :",
    "Date de naissance (format exemple: 05/09/2002) :"
]


class Windows:
    def __init__(self) -> None:
        self.layout = Layout()
        self.values = None
        self.command = True
        self.layout.split_column(Layout(name="message", size=3), Layout(name="main"))
        self.layout["main"].split_row(Layout(name="menu"), Layout(name="view_1", ratio=3), Layout(name="view_2", ratio=3))
        self.widgets = {
            "empty": SelectBox("", []),
            "Menu": SelectBox("Menu", MAIN_MENU, active=True),
            # Players
            "Players":  SelectBox("Players", PLAYERS_MENU, active=True),
            "Players register":  SelectBox("Players register", [], active=True),
            "input player": InputBox(PLAYER_INPUT, active=True),
            # Tournament
            "Tournament":  SelectBox("Tournament", TOURNAMENT_MENU, active=True),
            "tournament_input": SelectBox("new tournament", ["Add player", "Start tournament"]),
            # a tester
            #"valid_input":  SelectBox("Validation", ["Validation", "Back without validation"]),
            #"test": SelectBox('test', ['test'])
        }
        self.views = {
            "menu": self.widgets["Menu"],
            "view_1": self.widgets["empty"],
            "view_2": self.widgets["empty"],
        }
        self.views["menu"].active = True

    def show(self):
        for view, table_object in self.views.items():
            self.layout[view].update(table_object.get_table())

    def keyboard(self):
        input_char = msvcrt.getch()
        if self.command:
            if input_char == b'\x03': # ctrl + c
                self.run = False
            elif input_char == b's' or input_char == b'z':
                self.views["menu"].select(input_char)
                self.show()
            elif input_char == b'd' or input_char == b'q':
                #self.layout_move(input_char)
                pass
            elif input_char == b'\r':
                value = self.views["menu"].get_values()
                self.view_controller(value)
        
        else:
            self.views["view_1"].update(input_char)
            if not self.views["view_1"].table:
                self.command = True
                self.widgets["input player"].__init__(PLAYER_INPUT) # faire une loop reinitialiser tout les objet input dans widget
                self.views["view_1"] = self.widgets["empty"]
                self.views["menu"].active = True
            self.show()

    def view_controller(self, value):
        match value:
            case "Players":
                self.views["menu"] = self.widgets["Players"]
            case "Add player":
                self.views["view_1"] = self.widgets["input player"]
                self.command = False
                self.widgets["Players"].active = False
            case "Players register":
                self.views["menu"] = self.widgets["Players register"]
            case "Tournament":
                self.views["menu"] = self.widgets["Tournament"]
            case "Back":
                self.views["menu"] = self.widgets["Menu"]
            case "Quit":
                self.run = False
        self.show()

    def live(self):
        self.run = True
        self.show()
        with Live(self.layout, refresh_per_second=20):
            while self.run:
                self.keyboard()


if __name__ == "__main__":
    w = Windows()
    w.live()
