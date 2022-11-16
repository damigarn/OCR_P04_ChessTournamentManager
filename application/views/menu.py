class MenuView:

    @staticmethod
    def home():
        print("\n-------------- HOME --------------\n"
              "[1] Set up a new tournament\n"
              "[2] Start/Resume a tournament\n"
              "[3] Add a player to the database\n"
              "[4] Update Elo rating of a player\n"
              "[5] Reports\n"
              "[6] Quit application\n"
              "----------------------------------\n"
              "Enter your [option]: ", end='')

    @staticmethod
    def user_option():
        return input("Enter your [option]: ").lower()

    def user_confirm(self, prompt: str):
        while True:
            response = input(f"{prompt} [y] or [N]: ").lower()
            if response not in ["y", "n"]:
                self.invalid_input()
            if response == "y":
                return True
            if response == "n":
                self.operation_cancelled()
                return False

    @staticmethod
    def invalid_input():
        print("Invalid input. Enter a valid [option].")

    @staticmethod
    def operation_cancelled():
        print("Operation cancelled.")

    @staticmethod
    def operation_success():
        print("Operation successful.")

    @staticmethod
    def pause():
        input("Press [Enter] to continue")
