from tinydb import TinyDB

from utils import DB_TOURNAMENTS


db = TinyDB(DB_TOURNAMENTS, indent=4)


class Tournament:

    def __init__(self,
                 name: str,
                 location: str,
                 time_control: str,
                 description: str,
                 players: list,
                 id_tournament: int = 0,
                 start_date: str = "Not started",
                 end_date: str = "Not finished",
                 current_round: str = 0,
                 rounds_max: int = 4,
                 rounds: list = []
                 ):
        self.name = name.title()
        self.location = location.capitalize()
        self.time_control = time_control
        self.description = description
        self.players = players
        self.id_tournament = id_tournament
        self.start_date = start_date
        self.end_date = end_date
        self.current_round = current_round
        self.rounds_max = rounds_max
        self.rounds = rounds

    def serialize(self):
        """
        Return a serialized instance of a tournament
        :return: A serialized instance
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
                "rounds": self.rounds}

    def add_tournament_to_db(self):
        """
        Add a tournament to the database
        """
        # Astuce pour obtenir un id_tournament unique
        # égale au doc_id généré par TinyDB :
        # La méthode insert() retourne le doc_id
        # de l'enregistrement à son exécution
        id_new_t = db.insert(self.serialize())
        db.update({"id_tournament": str(id_new_t)}, doc_ids=[id_new_t])

    @staticmethod
    def load(id_t):
        """
        Load one tournament of the database
        :param id_t: id_tournament
        :return: Infos of one tournament
        """
        t = db.get(doc_id=id_t)
        if t is not None:
            return Tournament(id_tournament=t['id_tournament'],
                              name=t['name'],
                              location=t['location'],
                              start_date=t['start_date'],
                              end_date=t['end_date'],
                              time_control=t['time_control'],
                              description=t['description'],
                              rounds_max=t['rounds_max'],
                              current_round=t['current_round'],
                              players=t['players'],
                              rounds=t['rounds'])
        else:
            return None

    @staticmethod
    def load_all():
        """
        Load all the tournaments of the database
        :return: List of all tournaments
        """
        return db.all()

    def update(self, key, value):
        """
        Update an info of a tournament
        :param key: key of the info
        :param value: new value of the info
        """
        db.update({key: value}, doc_ids=[int(self.id_tournament)])

    def update_rounds(self, new_round):
        """
        Update the rounds infos of a tournament
        :param new_round: new_round
        """
        rounds = db.get(doc_id=self.id_tournament)["rounds"]
        rounds.pop(-1)
        rounds.append(new_round)
        db.update({'rounds': rounds}, doc_ids=[int(self.id_tournament)])


class Round:

    def __init__(self,
                 name: str,
                 start_date: str,
                 end_date: str,
                 matches: list):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = matches

    def serialize(self):
        """
        Generate a serialized instance of a round
        :return:
        """
        return {"name": self.name,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "matches": self.matches}
