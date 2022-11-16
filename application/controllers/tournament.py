from datetime import datetime

from application.views.menu import MenuView
from application.models.player import Player
from application.views.tournament import TournamentViews
from application.models.tournament import Tournament, Round
from application.controllers.reports import ReportControl

NOW = datetime.now().strftime("%d/%m/%Y - %H:%M")


class TournamentControl:

    @staticmethod
    def new_tournament():
        """
        Control the actions to add a new tournament to the database
        :return:
        """
        TournamentViews.header_new_tournament()

        # Name input
        name = TournamentViews.tournament_info_input("name")

        # Location input
        location = TournamentViews.tournament_info_input("location")

        # Time control input
        TournamentViews.time_control()
        while True:
            tc = TournamentViews.tournament_info_input("time control")
            if tc == "1":
                time_control = "Bullet"
                break
            if tc == "2":
                time_control = "Blitz"
                break
            if tc == "3":
                time_control = "Rapid"
                break
            else:
                MenuView.invalid_input()

        # Description input
        description = TournamentViews.tournament_info_input("description")

        # Players selection
        available_players = [item['id_player'] for item in Player.load_all()]
        players = []
        ReportControl.all_players("1")  # "1" for alphabetic order
        print("Choose 8 players in this list.\n"
              "Enter the [Id] of:")
        for i in range(1, 9):
            while True:
                id_player = input(f"  - Player{i}: ")
                if id_player in available_players:
                    players.append({"id_player": id_player,
                                    "total_score": 0.0})
                    available_players.remove(id_player)
                    break
                else:
                    print("Invalid [option] or player already already chosen.")

        # New tournament instance
        new_tournament = Tournament(name,
                                    location,
                                    time_control,
                                    description,
                                    players)

        # Add new tournament instance to the database
        Tournament.add_tournament_to_db(new_tournament)

        print("Tournament successfully saved and ready to start.")

    def start_resume_tournament(self):
        """
        Control the actions to manage a tournament and rounds
        :return:
        """

        # List of active tournament
        db_import = []
        for item in Tournament.load_all():
            if item['end_date'] == 'Not finished':
                db_import.append(item)

        # Heading of the table
        tournaments = [["Id",
                        "Name",
                        "Location",
                        "Start date",
                        "Time control",
                        "Current round"]]

        # Rows of the table
        for item in db_import:
            tournaments.append([item['id_tournament'],
                                item['name'],
                                item['location'],
                                item['start_date'],
                                item['time_control'],
                                item['current_round']])

        # Show table of active tournaments
        TournamentViews.active_tournaments(tournaments)

        # Input choice tournament
        id_available = [item['id_tournament'] for item in db_import]
        while True:
            id_t_input = input("Enter the tournament [Id] to start/resume: ")
            if id_t_input in id_available:
                self.start_round_or_end_round(id_t_input)
                break
            else:
                print("Invalid [option]. ", end='')

    def start_round_or_end_round(self, id_t):

        # Tournament infos
        tournament = Tournament.load(id_t)

        # Last tournament round status
        if len(tournament.rounds) > 0:
            last_round = tournament.rounds[-1]

            # If end_date round is "Not finished"
            if last_round["end_date"] == "Not finished":
                self.end_round(id_t)
            else:
                self.start_round(id_t)
        else:
            self.start_round(id_t)

    def start_round(self, id_t):
        """
        Manage to start a round
        :return:
        """
        t = Tournament.load(id_t)
        current_round = t.current_round

        if MenuView().user_confirm("Do you want to "
                                   "start the next round?"):
            # Si premier round
            if current_round == 0:
                self.start_tournament(id_t)
            # Si autre round
            elif current_round > 0:
                self.new_round(id_t)

    def start_tournament(self, id_t):

        t = Tournament.load(id_t)

        # Start date update
        t.update("start_date", NOW)

        # Create new round
        self.new_round(id_t)

    def new_round(self, id_t):

        t = Tournament.load(id_t)

        # Tournament current round update
        t.current_round += 1
        t.update("current_round", t.current_round)

        # Match lists
        m_to_db = self.swiss_pairing(id_t)[0]
        m_to_display = self.swiss_pairing(id_t)[1]

        matches_table = [["", "Player 1", "VS", "Player 2"]]
        matches_table.extend([f"Match {int(m_to_display.index(i)) + 1}",
                              i[0],
                              "VS",
                              i[1]] for i in m_to_display)
        TournamentViews.next_round(matches_table)

        # Tournament rounds list update
        new_round = Round(name=f"Round {t.current_round}",
                          start_date=NOW,
                          end_date="Not finished",
                          matches=m_to_db)
        t.rounds.append(new_round.serialize())
        t.update("rounds", t.rounds)
        print("Round started.")
        input("Press [Enter] to continue")

    @staticmethod
    def end_round(id_t):

        # Tournament infos
        tournament = Tournament.load(id_t)

        # Last round saved for the tournament
        round_to_end = tournament.rounds[-1]

        # Matches list from the last round
        matches = round_to_end["matches"]
        matches_table = [["", "Player 1", "VS", "Player 2"]]
        for i in matches:
            match_name = f"Match {int(matches.index(i)) + 1}"
            player1 = Player.full_name(matches[matches.index(i)][0][0])
            player2 = Player.full_name(matches[matches.index(i)][1][0])
            matches_table.append([match_name, player1, "VS", player2])
        TournamentViews.next_round(matches_table)

        # Confirm ending round
        if MenuView().user_confirm("If you confirm the end of the round,\n"
                                   "you will be asked to give the matches "
                                   "results. \nDo you confirm the end "
                                   "of the round?"):

            # Ask results and put scores in matches list
            print("\nREMINDER FOR RESULTS INPUT:\n"
                  "[1] Player 1 wins, [2] Player 2 wins, [3] Draw")
            for i in matches:
                match_index = int(matches.index(i)) + 1
                result = TournamentViews.match_result(match_index)
                if result == "1":
                    matches[matches.index(i)][0][1] = 1.0
                elif result == "2":
                    matches[matches.index(i)][1][1] = 1.0
                elif result == "3":
                    matches[matches.index(i)][0][1] = 0.5
                    matches[matches.index(i)][1][1] = 0.5

            # Tournaments players id and scores from the database
            players = tournament.players

            # Add scores from the round to the players scores
            players_dict = {i["id_player"]: i for i in players}

            for i in matches:
                id_p1 = i[0][0]
                score_p1 = i[0][1]
                id_p2 = i[1][0]
                score_p2 = i[1][1]
                players_dict[id_p1]['total_score'] += score_p1
                players_dict[id_p2]['total_score'] += score_p2

            players.clear()
            for value in players_dict.values():
                players.append(value)

            # Update player scores and rounds list in database

            round_to_end['end_date'] = NOW
            round_to_end['matches'] = matches

            tournament.update("players", players)
            tournament.update_rounds(round_to_end)

            # Check if tournament is finished
            if tournament.current_round == tournament.rounds_max:
                tournament.update("end_date", NOW)
                print("\n==================================================\n"
                      "TOURNAMENT IS FINISHED. HERE IS THE FINAL RANKING.\n"
                      "==================================================")

            # Show players ranking
            ReportControl.tournament_players(tournament.id_tournament, "2")
            input("Press [Enter] to continue")

    @staticmethod
    def swiss_pairing(id_t):
        """
        Generate the pairs for matches following swiss pairing method
        :param id_t:
        :return:
        """
        t = Tournament.load(id_t)

        # Tournament status
        current_round = t.current_round

        # Tournament's players import from database
        # [{"id_player": id1, "total_score": 0.0},
        # {"id_player": id2, "total_score": 0.0},
        # ...]
        t_players = t.players

        # Adding elo_rating to each player dictionary
        for item in t_players:
            item["elo_rating"] = Player.load(item["id_player"]).elo_rating

        # Converting players dictionaries to list for ordering
        # [[id_player1, total_score1, elo_rating1], [id2, t_s2, e_r2],...]
        players = [[item["id_player"],
                    item["total_score"],
                    item["elo_rating"]] for item in t_players]

        # List ordered by elo_rating decreasing
        players.sort(key=lambda x: x[2], reverse=True)

        # List of matches returned by the function
        db_format = []  # [[id_player1, 0.0], [id_player1, 0.0]]
        display_format = []  # "[Fullname Player1, Fullname Player2]"

        """
        If it is the first round of the tournament :
        """
        if current_round == 1:

            # List divided by 2
            players_sup = players[:4]
            players_inf = players[-4:]

            # Pairing for matches
            for player in range(len(players_sup)):
                # DB_FORMAT
                player1 = players_sup[player][0]
                player2 = players_inf[player][0]
                db_format.append([[player1, 0.0], [player2, 0.0]])
                # DISPLAY FORMAT
                display_format.append([Player.full_name(player1),
                                       Player.full_name(player2)])

        """
        If it is not the first round of the tournament
        """
        if current_round > 1:

            # All matches played (raw import)
            raw_matches = [item['matches'] for item in t.rounds]
            # raw_matches = [[[[id_player1, score1], [id_p2, sc2]],
            #                 [[id_p1, sc1], [id_p2, sc2]], ...]]

            # Matches list simplifier
            matches = []
            for player in raw_matches:
                round_matches = player
                for match in round_matches:
                    matches.append((match[0][0], match[1][0]))
            # matches = [(id_p1, id_p2), (id_p1, id_p2), (id_p1, id_p2), ...]

            # List of players ordered by total_score decreasing
            # (already ordered by elo_rating decreasing)
            players.sort(key=lambda x: x[1], reverse=True)

            # List of players ids to iterate for pairing later
            available_p = [player[0] for player in players]
            # Used to iterate or not on a player
            affected_p = []

            # Pairing
            for _ in range(4):

                # First player of the available players list
                player = available_p[0]

                # To select next opponent in the list
                n = 1
                # Check if the pairing (player, opponent)
                # already exists in all matches played in
                # the tournament and affect the next player
                # for opponent and check again the pairing
                # and so on
                while True:
                    # Opponent is the next player in the list
                    opponent = available_p[available_p.index(player) + n]
                    if (player, opponent) in matches:
                        n += 1
                        continue
                    if (opponent, player) in matches:
                        n += 1
                        continue
                    break

                # Adding the pairing to the matches lists
                db_format.append([[player, 0.0], [str(opponent), 0.0]])
                display_format.append([Player.full_name(player),
                                       Player.full_name(str(opponent))])

                # Adding match players to the affected players list
                affected_p.append(player)
                affected_p.append(opponent)

                # Removing match players from available players list
                available_p.remove(player)
                available_p.remove(opponent)

        return db_format, display_format
