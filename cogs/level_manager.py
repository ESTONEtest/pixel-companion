from utils.logger import logger


class LevelManager:


    # ==================================================
    # LEVEL REQUIREMENTS
    # ==================================================

    LEVELS = {

        1: 0,
        2: 100,
        3: 300,
        4: 600,
        5: 1000,
        6: 1500,
        7: 2200,
        8: 3000,
        9: 4000,
        10: 5500,

    }



    # ==================================================
    # GET LEVEL BY XP
    # ==================================================

    def get_level(
        self,
        xp: int
    ):

        level = 1


        for lvl, needed_xp in self.LEVELS.items():

            if xp >= needed_xp:

                level = lvl


        return level



    # ==================================================
    # CHECK LEVEL UP
    # ==================================================

    def check_level_up(
        self,
        old_level: int,
        xp: int
    ):

        new_level = self.get_level(
            xp
        )


        if new_level > old_level:

            logger.info(
                f"Level up: {old_level} -> {new_level}"
            )

            return new_level


        return False



    # ==================================================
    # NEXT LEVEL XP
    # ==================================================

    def next_level_xp(
        self,
        level: int
    ):

        return self.LEVELS.get(
            level + 1,
            None
        )



level_manager = LevelManager()