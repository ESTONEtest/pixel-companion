import random


class CriticalSystem:

    BASE_CRIT_CHANCE = 10
    MAX_CRIT_CHANCE = 50

    # ==================================================
    # CRITICAL CHANCE
    # ==================================================

    def is_critical(
        self,
        luck: int
    ) -> bool:

        chance = max(
            0,
            min(
                self.BASE_CRIT_CHANCE + luck,
                self.MAX_CRIT_CHANCE
            )
        )

        return random.randint(
            1,
            100
        ) <= chance


critical_system = CriticalSystem()