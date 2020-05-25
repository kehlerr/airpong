
class BattleModification:
    def __init__(self, name, battle, time=None):
        self.name = name
        self.battle = battle
        self.time = time

    def modify(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

class AddBalls(BattleModification):
    def modify(self):
        self.battle.add_ball_to_battle()
    
