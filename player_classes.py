# YACulator: player_classes.py
class Player:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team

class WR(Player):
    def __init__(self, name, team):
        super().__init__(name, 'WR', team)
        self.stats = {}

class DB(Player):
    def __init__(self, name, team, role):
        super().__init__(name, 'DB', team)
        self.role = role  # slot, wide, safety
        self.coverage_stats = {}

# Add other positions: QB, RB, TE as needed
