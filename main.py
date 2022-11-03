from models.player import Player
from models.tournament import Tournament
from models.round import Round

if __name__ == '__main__':
    Round.save_round_to_db(Round(1, "Round 1", "01/01/1900", "02/01/1900", []))
