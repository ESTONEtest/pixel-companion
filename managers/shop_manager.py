from managers.database import database
from managers.item_manager import item_manager
from utils.logger import logger


class ShopManager:


    # ==================================================
    # SHOP ITEMS
    # ==================================================

    SHOP = {


        "wooden_sword": {

            "price": 100

        },


        "iron_sword": {

            "price": 500

        },


        "leather_armor": {

            "price": 300

        },


        "crystal": {

            "price": 50

        }


    }



    # ==================================================
    # GET SHOP
    # ==================================================

    def get_shop(self):

        return self.SHOP



    # ==================================================
    # GET PRICE
    # ==================================================

    def get_price(
        self,
        item_id: str
    ):


        item = self.SHOP.get(
            item_id
        )


        if not item:

            return None


        return item["price"]



    # ==================================================
    # BUY ITEM
    # ==================================================

    def buy_item(
        self,
        user_id: int,
        item_id: str
    ):


        price = self.get_price(
            item_id
        )


        if price is None:

            return False



        player = database.get_user(
            user_id
        )


        if not player:

            return False



        if player["coins"] < price:

            return False



        database.execute(
            """
            UPDATE users
            SET coins = coins - ?
            WHERE user_id = ?
            """,
            (
                price,
                user_id
            )
        )


        logger.info(
            f"{user_id} bought {item_id}"
        )


        return True



shop_manager = ShopManager()