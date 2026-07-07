# ==================================================
# LEVEL MANAGER
# Pixel Companion RPG v2.0
# ==================================================


class LevelManager:


    def __init__(self):

        self.levels = {

            1: 0,
            2: 100,
            3: 250,
            4: 450,
            5: 700,

            6: 1000,
            7: 1400,
            8: 1900,
            9: 2500,
            10: 3200,

            15: 6000,
            20: 10000,
            25: 15000,
            30: 22000,

            35: 30000,
            40: 40000,
            50: 60000,

            60: 85000,
            75: 120000
        }



    # ==================================================
    # XP -> LEVEL
    # ==================================================

    def get_level(
        self,
        xp: int
    ):

        current_level = 1


        for level, required_xp in sorted(
            self.levels.items()
        ):

            if xp >= required_xp:

                current_level = level

            else:

                break


        return current_level



    # ==================================================
    # LEVEL -> XP
    # ==================================================

    def get_xp_for_level(
        self,
        level: int
    ):

        if level in self.levels:

            return self.levels[level]


        return level * level * 100



    # ==================================================
    # NEXT LEVEL
    # ==================================================

    def get_next_level_xp(
        self,
        level: int
    ):

        return self.get_xp_for_level(
            level + 1
        )



level_manager = LevelManager()