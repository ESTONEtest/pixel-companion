import random


class LootDropSystem:

    # ==================================================
    # SETTINGS
    # ==================================================

    DROP_CHANCE = 60

    # ==================================================
    # ITEM NAMES
    # ==================================================

    ITEM_NAMES = {
        "wood": "🪵 Дерево",
        "iron": "⛓️ Железо",
        "crystal": "💎 Кристалл",
        "potion": "🧪 Зелье"
    }

    # ==================================================
    # LOOT TABLE
    # ==================================================

    LOOT_TABLE = [

        {
            "item": "wood",
            "weight": 35
        },

        {
            "item": "iron",
            "weight": 25
        },

        {
            "item": "crystal",
            "weight": 15
        },

        {
            "item": "potion",
            "weight": 10
        }

    ]

    # ==================================================
    # FORMAT LOOT
    # ==================================================

    def format_loot(
        self,
        loot: str | None
    ):

        if not loot:
            return "Нет"

        return self.ITEM_NAMES.get(
            loot,
            loot
        )

    # ==================================================
    # ROLL LOOT
    # ==================================================

    def roll_loot(self):

        if random.randint(1, 100) > self.DROP_CHANCE:
            return None

        items = []
        weights = []

        for loot in self.LOOT_TABLE:

            items.append(
                loot["item"]
            )

            weights.append(
                loot["weight"]
            )

        return random.choices(
            items,
            weights=weights,
            k=1
        )[0]


loot_drop_system = LootDropSystem()