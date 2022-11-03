from tinydb import TinyDB

from utils import DB_ROUNDS


db = TinyDB(DB_ROUNDS, indent=4)


class Round:

    def __init__(self,
                 id_tournament: int,
                 name: str,
                 start_date: str,
                 end_date: str,
                 matches: list,
                 id_round: int = 0):
        self.id_tournament = id_tournament
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = matches
        self.id_round = id_round

    def serialize_round(self):
        """
        Generate a serialized instance of a round
        :return:
        """
        return {"id_round": self.id_round,
                "id_tournament": self.id_tournament,
                "name": self.name,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "matches": self.matches}

    def generate_pairs(self, players):
        """
        Generate the pairs of player to constitute the matches of a round
        :param players: List of players
        :return: List of matches as tuples formated as [(Player1, Player2), (Player1, Player2)...]
        """
        pass

    def start_round(self):
        """
        Start a round
        :return:
        """
        pass

    def terminate_round(self):
        """
        Terminate a round with the list of matches and their score
        :return: List of matches as tuples formatted as ([Player1, score], [Player2, score])
        """
        pass

    def save_round_to_db(self):
        """
        Save a round to the database
        :return:
        """
        # Si enregistrement du premier round, gestion d'erreur d'index pour 'db.all()[-1]'
        try:
            self.id_round = db.all()[-1].doc_id + 1
        except IndexError:
            self.id_round = 1
        db.insert(self.serialize_round())
        print("Round successfully saved")

