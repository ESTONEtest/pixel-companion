import random


class MonsterManager:

    MONSTERS = {

        "slime": {
            "name": "Слизень",
            "icon": "🟢",
            "min_level": 1,
            "hp": 35,
            "attack": 4,
            "defense": 0,
            "reward_xp": 15,
            "reward_coins": 20
        },

        "goblin": {
            "name": "Гоблин",
            "icon": "🗡️",
            "min_level": 1,
            "hp": 55,
            "attack": 7,
            "defense": 1,
            "reward_xp": 30,
            "reward_coins": 40
        },

        "skeleton": {
            "name": "Скелет",
            "icon": "💀",
            "min_level": 2,
            "hp": 95,
            "attack": 12,
            "defense": 3,
            "reward_xp": 60,
            "reward_coins": 85
        },

        "dark_knight": {
            "name": "Темный рыцарь",
            "icon": "⚔️",
            "min_level": 4,
            "hp": 180,
            "attack": 20,
            "defense": 7,
            "reward_xp": 130,
            "reward_coins": 180
        },

        "demon": {
            "name": "Демон",
            "icon": "🔥",
            "min_level": 7,
            "hp": 320,
            "attack": 32,
            "defense": 12,
            "reward_xp": 300,
            "reward_coins": 500
        }

    }

    # ==================================================
    # GET RANDOM MONSTER
    # ==================================================

    def get_random_monster(self):

        monster_id = random.choice(
            list(self.MONSTERS.keys())
        )

        return self.get_monster(
            monster_id
        )

    # ==================================================
    # GET RANDOM MONSTER FOR PLAYER
    # ==================================================

    def get_random_monster_for_player(
        self,
        player: dict
    ):

        level = player["level"]

        available_monsters = []

        for monster_id, monster in self.MONSTERS.items():

            if monster["min_level"] <= level:

                available_monsters.append(
                    monster_id
                )

        if not available_monsters:

            available_monsters = [
                "slime"
            ]

        monster_id = random.choice(
            available_monsters
        )

        return self.get_monster(
            monster_id
        )

    # ==================================================
    # GET MONSTER
    # ==================================================

    def get_monster(
        self,
        monster_id: str
    ):

        monster = self.MONSTERS[monster_id].copy()

        monster["id"] = monster_id

        monster["display_name"] = (
            f"{monster['icon']} {monster['name']}"
        )

        return monster


monster_manager = MonsterManager()