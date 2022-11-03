from tinydb import TinyDB

from models.round import Round
from utils import DB_TOURNAMENTS


db = TinyDB(DB_TOURNAMENTS, indent=4)


class Tournament:

    def __init__(self,
                 name: str,
                 location: str,
                 time_control: str,
                 description: str,
                 rounds_max: int,
                 players: list,
                 rounds: list,
                 ranking: list,
                 id_tournament: int = 0,
                 start_date: str = "Not started",
                 end_date: str = "Not finished",
                 current_round: str = 0
                 ):
        self.name = name.title()
        self.location = location.capitalize()
        self.time_control = time_control
        self.description = description
        self.rounds_max = rounds_max
        self.players = players
        self.rounds = rounds
        self.ranking = ranking
        self.id_tournament = id_tournament
        self.start_date = start_date
        self.end_date = end_date
        self.current_round = current_round

    def serialize_tournament(self):
        """
        Generate a serialized instance of a tournament
        :return:
        """
        return {"id_tournament": self.id_tournament,
                "name": self.name,
                "location": self.location,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "time_control": self.time_control,
                "description": self.description,
                "rounds_max": self.rounds_max,
                "current_round": self.current_round,
                "players": self.players,
                "rounds": self.rounds,
                "ranking": self.ranking}

    def save_tournament_to_db(self):
        """
        Save a tournament to the database
        :return:
        """
        # Si enregistrement du premier tournoi, gestion d'erreur d'index pour 'db.all()[-1]'
        try:
            self.id_tournament = db.all()[-1].doc_id + 1
        except IndexError:
            self.id_tournament = 1

        db.insert(self.serialize_tournament())
        print(f"Tournament ‘{self.name} in {self.location}' successfully saved")

    def start_tournament(self):
        pass

    def update_tournament(self):
        pass
