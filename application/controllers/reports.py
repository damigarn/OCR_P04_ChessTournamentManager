from application.models.player import Player
from application.models.tournament import Tournament
from application.views.reports import ReportViews


class ReportControl:

    def __init__(self):

        self.v_reports = ReportViews()

    def menu(self):
        """
        Reports menu management
        :return: None
        """
        self.v_reports.header()
        self.v_reports.menu()

        user_response = input()

        # All players
        if user_response == "1":
            while True:
                order = self.v_reports.order_list()
                if self.all_players(order):
                    break
                self.v_reports.invalid_input()
                print("")

        # All tournaments
        elif user_response == "2":
            self.all_tournaments()

        # Players of a tournament
        elif user_response == "3":
            self.all_tournaments()
            while True:
                id_t = self.v_reports.id_tournament_input()
                if self.check_exist_tournament(id_t):
                    while True:
                        order = self.v_reports.order_list()
                        if self.tournament_players(id_t, order):
                            break
                        self.v_reports.invalid_input()
                        print("")
                    break
                else:
                    self.v_reports.invalid_input()

        # Rounds of a tournament
        elif user_response == "4":
            self.all_tournaments()
            while True:
                id_t = self.v_reports.id_tournament_input()
                if self.check_exist_tournament(id_t):
                    self.tournament_rounds(id_t)
                    break
                else:
                    self.v_reports.invalid_input()

        # Matches of a tournament
        elif user_response == "5":
            self.all_tournaments()
            while True:
                id_t = self.v_reports.id_tournament_input()
                if self.check_exist_tournament(id_t):
                    self.tournament_matches(id_t)
                    break
                else:
                    self.v_reports.invalid_input()

        # Back Home menu
        elif user_response == "6":
            self.back_home()
            return

        # Invalid input
        else:
            self.v_reports.invalid_input()
            print("")
            self.menu()

        self.hit_continue()
        self.menu()

    @staticmethod
    def back_home():
        """
        Asking if user want to see another
        report or going back to the home menu
        after each report
        :return:
        """
        from application.controllers.application import Application
        Application().home()

    @staticmethod
    def hit_continue():
        input("Press [Enter] to continue")

    @staticmethod
    def all_players(order):

        if order not in ["1", "2"]:
            return False

        db_import = Player.load_all()
        if order == "1":
            db_import.sort(key=lambda x: x['lastname'])
        if order == "2":
            db_import.sort(key=lambda x: x['elo_rating'], reverse=True)

        players = [["Id",
                    "Lastname",
                    "Firstname",
                    "Birthday",
                    "Gender",
                    "Elo Rating"]]

        for item in db_import:
            players.append([item['id_player'],
                            item['lastname'],
                            item['firstname'],
                            item['birthday'],
                            item['gender'],
                            item['elo_rating']])
        if order == "1":
            ReportViews.all_players("in alphabetical order", players)
        if order == "2":
            ReportViews.all_players("ordered by the Elo rating", players)

        return True

    @staticmethod
    def all_tournaments():

        db_import = Tournament.load_all()

        tournaments = [["Id",
                        "Name",
                        "Location",
                        "Start date",
                        "End date",
                        "Time control",
                        "Description",
                        "Current round"]]

        for item in db_import:
            tournaments.append([item['id_tournament'],
                                item['name'],
                                item['location'],
                                item['start_date'],
                                item['end_date'],
                                item['time_control'],
                                item['description'],
                                item['current_round']])

        ReportViews.all_tournaments(tournaments)

    @staticmethod
    def tournament_players(id_tournament, order):

        if order not in ["1", "2"]:
            return False

        t = Tournament.load(id_tournament)
        tournament = t.name

        # Liste brute de dictionnaires provenant
        # de la database tournaments.json
        # {'id_player',  'total_score'}
        tournament_players_raw = t.players

        # Séparation en deux listes des id_players
        # et des total_score
        t_id_players = [i['id_player'] for i in tournament_players_raw]
        t_scores_players = [i['total_score'] for i in tournament_players_raw]

        # Liste de dictionnaires contenant
        # l'ensemble des infos de chaque joueur du tournoi
        t_players = []
        for i in t_id_players:
            p = Player.load(i)
            player = {'id_player': p.id_player,
                      'lastname': p.lastname,
                      'firstname': p.firstname,
                      'birthday': p.birthday,
                      'gender': p.gender,
                      'elo_rating': p.elo_rating,
                      'total_score': t_scores_players[t_id_players.index(i)]}
            t_players.append(player)

        # Pre-ordering (corresponding to order = "1" in arg)
        t_players.sort(key=lambda x: x['lastname'])
        t_players.sort(key=lambda x: x['elo_rating'], reverse=True)

        # Ordering list
        if order == "2":
            t_players.sort(key=lambda x: x['total_score'], reverse=True)

        # Table heading
        players = [["Id",
                    "Lastname",
                    "Firstname",
                    "Birthday",
                    "Gender",
                    "Elo Rating",
                    "Total score"]]

        # Adding table content
        for item in t_players:
            players.append([item['id_player'],
                            item['lastname'],
                            item['firstname'],
                            item['birthday'],
                            item['gender'],
                            item['elo_rating'],
                            item['total_score']])

        # Show table
        if order == "1":
            ReportViews.tournament_players(tournament,
                                           players,
                                           "in alphabetical order")
        if order == "2":
            ReportViews.tournament_players(tournament,
                                           players,
                                           "ordered by scores")

        return True

    @staticmethod
    def tournament_rounds(id_tournament):

        t = Tournament.load(id_tournament)
        tournament_name = t.name
        rounds_import = t.rounds

        rounds = [["Name",
                   "Start date",
                   "End date",
                   "Matches ([Player1, Score], [Player2, Score])"]]

        for item in rounds_import:
            raw_matches = item['matches']
            for i in raw_matches:
                id_player1 = i[0][0]
                i[0][0] = Player.full_name(id_player1)
                id_player2 = i[1][0]
                i[1][0] = Player.full_name(id_player2)
            matches = ""
            for match in raw_matches:
                matches = matches + str(match) + "\n"
            rounds.append([item['name'],
                           item['start_date'],
                           item['end_date'],
                           matches])

        ReportViews.tournament_rounds(tournament_name, rounds)

    @staticmethod
    def tournament_matches(id_tournament):

        t = Tournament.load(id_tournament)
        tournament = t.name
        matches_import = [item['matches'] for item in t.rounds]
        matches_loop = [item for sublist in matches_import for item in sublist]

        matches = [["Player 1", "Score", "", "Player 2", "Score"]]

        for item in matches_loop:
            matches.append([Player.full_name(item[0][0]),
                            item[0][1],
                            "VS",
                            Player.full_name(item[1][0]),
                            item[1][1]])

        ReportViews.tournament_matches(tournament, matches)

    @staticmethod
    def check_exist_tournament(id_tournament):
        if Tournament.load(id_tournament) is not None:
            return True
