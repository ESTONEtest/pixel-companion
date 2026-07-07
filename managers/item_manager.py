from utils.logger import logger


class ItemManager:

    # ==================================================
    # ITEMS DATABASE
    # ==================================================

    ITEMS = {

        "wood": {
            "name": "🪵 Дерево",
            "type": "material",
            "rarity": "Common",
            "attack": 0,
            "defense": 0,
            "luck": 0,
            "price": 15
        },

        "iron": {
            "name": "⛓️ Железо",
            "type": "material",
            "rarity": "Common",
            "attack": 0,
            "defense": 0,
            "luck": 0,
            "price": 30
        },

        "crystal": {
            "name": "💎 Кристалл",
            "type": "material",
            "rarity": "Rare",
            "attack": 0,
            "defense": 0,
            "luck": 0,
            "price": 50
        },

        "potion": {
            "name": "🧪 Зелье лечения",
            "type": "consumable",
            "rarity": "Common",
            "attack": 0,
            "defense": 0,
            "luck": 0,
            "heal": 30,
            "price": 75
        },

        "wooden_sword": {
            "name": "🗡 Деревянный меч",
            "type": "weapon",
            "rarity": "Common",
            "attack": 5,
            "defense": 0,
            "luck": 0,
            "price": 100
        },

        "iron_sword": {
            "name": "⚔ Железный меч",
            "type": "weapon",
            "rarity": "Uncommon",
            "attack": 15,
            "defense": 0,
            "luck": 0,
            "price": 300
        },

        "leather_armor": {
            "name": "🛡 Кожаная броня",
            "type": "armor",
            "rarity": "Common",
            "attack": 0,
            "defense": 10,
            "luck": 0,
            "price": 250
        }

    }

    # ==================================================
    # GET ITEM
    # ==================================================

    def get_item(
        self,
        item_id: str
    ):

        item = self.ITEMS.get(
            item_id
        )

        if item is None:

            logger.warning(
                f"Item not found: {item_id}"
            )

        return item

    # ==================================================
    # CHECK ITEM
    # ==================================================

    def exists(
        self,
        item_id: str
    ):

        return item_id in self.ITEMS

    # ==================================================
    # GET ALL ITEMS
    # ==================================================

    def get_all_items(self):

        return self.ITEMS


item_manager = ItemManager()