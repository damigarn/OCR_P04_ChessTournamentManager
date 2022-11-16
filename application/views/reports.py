from terminaltables import AsciiTable


class ReportViews:

    @staticmethod
    def header():
        print("\n------------ REPORTS ------------")

    @staticmethod
    def menu():
        print("All elements from the database: \n"
              "  [1] Players list\n"
              "  [2] Tournaments list\n"
              "From a tournament: \n"
              "  [3] Players list\n"
              "  [4] Rounds list\n"
              "  [5] Matches list\n"
              "[6] Return to home menu\n"
              "---------------------------------\n"
              "Enter your [option]: ", end='')

    @staticmethod
    def order_list():
        return input("\nOrder of the list:\n"
                     "[1] alphabetical\n"
                     "[2] ranking\n"
                     "Enter your [option]: ")

    @staticmethod
    def all_players(order, players):
        print(f"\nList of all the players in the database {order}:")
        print(AsciiTable(players).table)

    @staticmethod
    def all_tournaments(tournaments):
        print("\nList of all the tournaments in database:")
        print(AsciiTable(tournaments).table)

    @staticmethod
    def id_tournament_input():
        return input("Enter the [Id] of the tournament: ")

    @staticmethod
    def tournament_players(tournament, players, order):
        print(f"\nList of all the players from '{tournament}' {order}: ")
        print(AsciiTable(players).table)

    @staticmethod
    def tournament_rounds(tournament, rounds):
        print(f"\nList of all the rounds from {tournament}: ")
        print(AsciiTable(rounds).table)

    @staticmethod
    def tournament_matches(tournament, matches):
        print(f"\nList of all the matches from {tournament}: ")
        print(AsciiTable(matches).table)

    @staticmethod
    def invalid_input():
        print("Enter a valid [option]: ", end="")
