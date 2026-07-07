import random


class MonsterManager:

    MONSTERS = {

        "Goblin": {
            "hp": 80,
            "attack": 10,
            "defense": 2,
            "reward_xp": 40,
            "reward_coins": 50
        },

        "Skeleton": {
            "hp": 150,
            "attack": 20,
            "defense": 5,
            "reward_xp": 80,
            "reward_coins": 100
        },

        "Dark Knight": {
            "hp": 300,
            "attack": 35,
            "defense": 10,
            "reward_xp": 150,
            "reward_coins": 200
        },

        "Demon": {
            "hp": 600,
            "attack": 50,
            "defense": 18,
            "reward_xp": 300,
            "reward_coins": 500
        }

    }

    def get_random_monster(self):

        name = random.choice(
            list(self.MONSTERS.keys())
        )

        monster = self.MONSTERS[name].copy()
        monster["name"] = name

        return monster


monster_manager = MonsterManager()