from application.views.menu import MenuView
from application.models.player import Player
from application.views.player import PlayerViews
from application.controllers.reports import ReportControl


class PlayerControl:

    @staticmethod
    def new_player():

        # Header
        PlayerViews.header()

        # Infos asked
        info_player = ["lastname",
                       "firstname",
                       "birthday",
                       "gender ([M] for male, [F] for Female)",
                       "Elo rating"]

        infos = []
        for i in info_player:
            info = PlayerViews.player_info_input(i)
            if info == "back":
                MenuView.operation_cancelled()
                return
            infos.append(info)

        # New Player instance
        new_player = Player(lastname=infos[0],
                            firstname=infos[1],
                            birthday=infos[2],
                            gender=infos[3],
                            elo_rating=infos[4])

        # Confirmation of saving to database
        if MenuView().user_confirm(f"Do you want to save "
                                   f"{infos[1].title()} {infos[0].title()} "
                                   f"to the database?"):
            new_player.add_player_to_db()
            MenuView.operation_success()

    def update_elo_rating(self):

        # Show players list in alphabetic order ("1" arg)
        ReportControl.all_players("1")

        while True:
            id_player = input("Enter the [Id] of a player "
                              "to update the Elo rating: ")

            # id_player is correct
            if self.check_player_exist(id_player):

                player = Player.load(id_player)

                new_elo_rating = input("New Elo Rating: ")

                # if new elo_rating is a number
                if new_elo_rating.isdigit():

                    user = MenuView().user_confirm("Do you confirm "
                                                   "this change?")
                    if user is True:
                        player.update("elo_rating", new_elo_rating)
                        MenuView.operation_success()
                        break
                    elif user is False:
                        break
                else:
                    MenuView.invalid_input()
            else:
                MenuView.invalid_input()

    @staticmethod
    def check_player_exist(id_player):
        # Return True if Player.load(id_player) is not None
        return Player.load(id_player) is not None
