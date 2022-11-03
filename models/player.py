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

    def save_player_to_db(self):
        """
        Save a player to the database
        :return:
        """
        # Si enregistrement du premier joueur, gestion d'erreur d'index pour 'db.all()[-1]'
        try:
            self.id_player = db.all()[-1].doc_id + 1
        except IndexError:
            self.id_player = 1
        db.insert(self.serialize_player())
        print(f"Player ‘{self.firstname} {self.lastname}' successfully saved")

