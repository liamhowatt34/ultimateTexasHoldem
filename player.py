# player.py
class Player:
    def __init__(self, roll, wins=0, losses=0, ties=0) -> None:
        self.roll = roll
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def update_wins(self):
        self.wins += 1

    def update_losses(self):
        self.losses += 1

    def update_ties(self):
        self.ties += 1
