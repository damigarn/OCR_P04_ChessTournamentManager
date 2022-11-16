class PlayerViews:

    @staticmethod
    def header():
        print("\n------------ NEW PLAYER ------------\n"
              "Enter [back] anytime to cancel and to go back to Home menu.")

    @staticmethod
    def player_info_input(info):
        return input("Enter the player's " + info + ": ").lower()
