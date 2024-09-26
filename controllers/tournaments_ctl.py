from views.view import View
from models.tournaments_model import Tournament, TournamentsDb
from controllers.tournament import ActualTournament


class TournamentsCtl:
    def __init__(self) -> None:
        self.view = View()
        self.tournament_db = TournamentsDb()
        self.actual_tournament = ActualTournament()

    def tournaments_menu(self):
        running = True
        while running:
            menu = [
                ("1", "Create new tournament"),
                ("2", "Select tournament"),
                ("3", "View all tournaments"),
                ("4", "Back")
            ]
            choice = self.view.input_menu(menu)
            match choice:
                case "1":
                    self.create_new_tournament()
                case "2":
                    tournament = self.select_tournament()
                    if tournament:
                        self.actual_tournament.selected_tournament_menu(tournament)
                case "3":
                    self.all_tournaments()
                case "4":
                    running = False
                case _:
                    self.view.view_message("Invalid input !", error=True)

    def create_new_tournament(self) -> None:
        tournaments_name = [tournament.name for tournament in self.tournament_db.get_all_tournaments()]
        fields = {
            "name": "Tournament name: ",
            "place": "Tournament place: ",
            "number_of_round": "Number of round (4 round if no value): "
        }
        user_input = self.view.multiple_inputs(fields)

        if user_input.get("name") not in tournaments_name:
            rounds_number = user_input.get("number_of_round")
            try:
                rounds_number = int(rounds_number) if rounds_number else 4
            except ValueError:
                self.view.view_message("Round must be an integer in range 4 to 10 !", error=True)
            else:
                if 4 <= rounds_number <= 10:
                    tournament = Tournament(user_input.get("name"), user_input.get("place"), rounds_number)
                    self.tournament_db.save(tournament)
                    self.view.view_message(f"New tournament '{user_input.get('name')}' created !")
                else:
                    self.view.view_message("Round must be in range 4 to 10 !", error=True)
        else:
            self.view.view_message(f"Tournament: '{user_input.get('name')}' already exist !", error=True)

    def select_tournament(self) -> Tournament | None:
        if tournaments := self.tournament_db.get_all_tournaments():
            data = []
            for tournament in tournaments:
                data.append({
                    "Tournament name": tournament.name,
                    "Place": tournament.place,
                    "Number of round": str(tournament.number_of_round),
                    "Started": tournament.start if tournament.start else "No started",
                    "Ended": tournament.end if tournament.end else "No finished"
                })
            self.view.table_view("Select tournament", data, selection=True)
            choice = self.view.simple_input("Enter key tournament: ")
            choice = self._check_input_number(choice, len(tournaments))
            if choice:
                tournament = tournaments[choice - 1]
                self.view.view_message(f"Tournament '{tournament.name}' selected")
                return tournament
            else:
                self.view.view_message("Invalid input !", error=True)
        else:
            self.view.view_message("No tournament !", error=True)

    def all_tournaments(self) -> None:
        tournaments = self.tournament_db.get_all_tournaments()
        data = []
        for tournament in tournaments:
            data.append({
                "Tournament name": tournament.name,
                "Place": tournament.place,
                "Number of round": str(tournament.number_of_round),
                "Status": self._tournament_status(tournament)
            })
        self.view.table_view("Select tournament", data)
        self.view.enter_continue()

    @staticmethod
    def _check_input_number(choice: str, max_value: int) -> int | None:
        try:
            choice = int(choice)
        except ValueError:
            pass
        else:
            if 1 <= choice <= max_value:
                return choice

    @staticmethod
    def _tournament_status(tournament: Tournament) -> str:
        if tournament.start and tournament.end:
            return f"Finished it {tournament.end}"
        elif tournament.start and not tournament.end:
            return f"Started it {tournament.start} but no finished"
        else:
            return "No started"
