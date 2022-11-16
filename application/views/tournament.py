from terminaltables import AsciiTable


class TournamentViews:

    @staticmethod
    def header_new_tournament():
        print("\n---------- NEW TOURNAMENT ----------")

    @staticmethod
    def tournament_info_input(info):
        return input("Enter the tournament's " + info + ": ").lower()

    @staticmethod
    def time_control():
        print("Time control options:\n"
              "[1] Bullet\n"
              "[2] Blitz\n"
              "[3] Rapid")

    @staticmethod
    def active_tournaments(tournaments):
        print("\n---------- ACTIVE TOURNAMENTS ----------")
        print("List of active tournaments: ")
        print(AsciiTable(tournaments).table)

    @staticmethod
    def next_round(matches):
        print("\nNEXT ROUND MATCHES")
        print(AsciiTable(matches).table)

    @staticmethod
    def match_result(match_index):
        print(f"Result match {match_index}: ", end='')
        return input()
