from application.views.menu import MenuView
from application.controllers.player import PlayerControl
from application.controllers.tournament import TournamentControl
from application.controllers.reports import ReportControl


class Application:

    def __init__(self):

        self.menu = MenuView()
        self.c_player = PlayerControl()
        self.c_tournament = TournamentControl()
        self.c_reports = ReportControl()

    def home(self):
        """
        Home menu management
        :return:
        """
        self.menu.home()

        user_response = input()

        # Set up a new tournament
        if user_response == "1":
            self.c_tournament.new_tournament()

        # Start/Resume a tournament
        elif user_response == "2":
            self.c_tournament.start_resume_tournament()

        # Add a player to database
        elif user_response == "3":
            self.c_player.new_player()

        # Update player's Elo rating
        elif user_response == "4":
            self.c_player.update_elo_rating()

        # Reports menu
        elif user_response == "5":
            self.c_reports.menu()

        # Quit application with confirmation management
        elif user_response == "6":
            if self.menu.user_confirm("Do you want to quit the application?"):
                exit()

        # Invalid input
        else:
            self.menu.invalid_input()

        print("")
        self.home()
