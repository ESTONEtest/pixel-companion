from utils.logger import logger


class ItemManager:

    # ==================================================
    # ITEMS DATABASE
    # ==================================================

    ITEMS = {

        "wooden_sword": {
            "name": "🗡 Wooden Sword",
            "type": "weapon",
            "rarity": "Common",
            "attack": 5,
            "defense": 0,
            "luck": 0,
            "price": 100
        },

        "iron_sword": {
            "name": "⚔ Iron Sword",
            "type": "weapon",
            "rarity": "Uncommon",
            "attack": 15,
            "defense": 0,
            "luck": 0,
            "price": 300
        },

        "leather_armor": {
            "name": "🛡 Leather Armor",
            "type": "armor",
            "rarity": "Common",
            "attack": 0,
            "defense": 10,
            "luck": 0,
            "price": 250
        },

        "crystal": {
            "name": "💎 Crystal",
            "type": "material",
            "rarity": "Rare",
            "attack": 0,
            "defense": 0,
            "luck": 0,
            "price": 50
        }

    }

    # ==================================================
    # GET ITEM
    # ==================================================

    def get_item(
        self,
        item_id: str
    ):

        item = self.ITEMS.get(item_id)

        if item is None:
            logger.warning(f"Item not found: {item_id}")

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