from tinydb import TinyDB

from utils import DB_PLAYERS


db = TinyDB(DB_PLAYERS, indent=4)


class Player:

    def __init__(self,
                 lastname: str,
                 firstname: str,
                 birthday: str,
                 gender: str,
                 elo_rating: int,
                 id_player: int = 0):
        self.lastname = lastname.capitalize()
        self.firstname = firstname.capitalize()
        self.birthday = birthday
        self.gender = gender.capitalize()
        self.elo_rating = elo_rating
        self.id_player = id_player

    def serialize_player(self):
        """
        Generate a serialized instance of a player
        :return:
        """
        return {"id_player": self.id_player,
                "lastname": self.lastname,
                "firstname": self.firstname,
                "birthday": self.birthday,
                "gender": self.gender,
                "elo_rating": self.elo_rating}

    def add_player_to_db(self):
        """
        Add a player to the database
        """
        # Astuce pour obtenir un id_player unique
        # égal au doc_id généré par TinyDB :
        # La méthode insert() retourne le doc_id
        # de l'enregistrement à son exécution
        id_new_player = db.insert(self.serialize_player())
        db.update({'id_player': str(id_new_player)}, doc_ids=[id_new_player])

    @staticmethod
    def load(id_player):
        """
        Load one player of the database
        :param id_player: id_player
        :return: Infos of one player
        """
        p = db.get(doc_id=id_player)
        if p is not None:
            return Player(id_player=p['id_player'],
                          lastname=p['lastname'],
                          firstname=p['firstname'],
                          birthday=p['birthday'],
                          gender=p['gender'],
                          elo_rating=p['elo_rating'])
        return None

    @staticmethod
    def full_name(id_player):
        """
        Generate a fullname player from an id
        :param id_player: id_player
        :return: Player fullname
        """
        player = db.get(doc_id=id_player)
        return f"{player['firstname']} {player['lastname']}"

    @staticmethod
    def load_all():
        """
        Load all the players of the database
        :return: List of all players
        """
        return db.all()

    def update(self, key, value):
        """
        Update an info of a player
        :param key: key of the info
        :param value: new value of the info
        :return:
        """
        db.update({key: value}, doc_ids=[int(self.id_player)])
