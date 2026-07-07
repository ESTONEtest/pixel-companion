import random


class LootDropSystem:

    # ==================================================
    # LOOT TABLE
    # ==================================================

    LOOT_TABLE = [
        ("crystal", 20),
        ("iron", 15),
        ("wood", 25),
        ("potion", 10),
    ]

    # ==================================================
    # ROLL LOOT
    # ==================================================

    def roll_loot(self):

        for item, chance in self.LOOT_TABLE:

            if random.randint(1, 100) <= chance:
                return item

        return None


loot_drop_system = LootDropSystem()