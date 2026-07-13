# systems/wishes_manager.py

import json
import os
import random

from datetime import datetime, timedelta


class WishesManager:
    """
    Менеджер системы пожеланий Pixel Companion.

    Формат:

    assets/wishes/

        categories.json
        rarity.json

        smile.json
        rest.json
        luck_today.json

    """

    def __init__(
        self,
        wishes_folder="assets/wishes"
    ):

        self.wishes_folder = wishes_folder

        self.users = {}

        self.cooldown_minutes = 60

        self.categories = {}

        self.category_names = {}

        self.rarities = {}

        self.load_wishes()



    # ==================================================
    # LOAD
    # ==================================================

    def load_wishes(self):

        self.categories = {}

        self.category_names = {}

        self.rarities = {}


        if not os.path.exists(
            self.wishes_folder
        ):

            os.makedirs(
                self.wishes_folder
            )

            return


        self.load_categories()

        self.load_rarity()

        self.load_categories_files()



    # ==================================================
    # CATEGORIES.JSON
    # ==================================================

    def load_categories(self):

        path = os.path.join(
            self.wishes_folder,
            "categories.json"
        )


        if not os.path.exists(
            path
        ):

            return


        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                self.category_names = json.load(
                    file
                )


        except Exception:

            self.category_names = {}



    # ==================================================
    # RARITY.JSON
    # ==================================================

    def load_rarity(self):

        path = os.path.join(
            self.wishes_folder,
            "rarity.json"
        )


        if not os.path.exists(
            path
        ):

            return


        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                self.rarities = json.load(
                    file
                )


        except Exception:

            self.rarities = {}



    # ==================================================
    # LOAD WISH FILES
    # ==================================================

    def load_categories_files(self):


        for file in os.listdir(
            self.wishes_folder
        ):


            if not file.endswith(
                ".json"
            ):

                continue


            if file in (
                "categories.json",
                "rarity.json"
            ):

                continue



            path = os.path.join(
                self.wishes_folder,
                file
            )


            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(
                        f
                    )


                category = file.replace(
                    ".json",
                    ""
                )


                if not isinstance(
                    data,
                    dict
                ):

                    continue



                self.categories[category] = {

                    "name":
                        self.category_names.get(
                            category,
                            category
                        ),

                    "image":
                        f"{category}.png",

                    "rarity":
                        data.get(
                            "rarity",
                            "common"
                        ),

                    "wishes":
                        data.get(
                            "wishes",
                            []
                        )

                }


            except Exception:

                continue




    # ==================================================
    # INFO
    # ==================================================

    def get_categories(self):

        return list(
            self.categories.keys()
        )



    def get_category_name(
        self,
        category
    ):


        if category in self.categories:

            return self.categories[category]["name"]


        return category



    def get_total_wishes(self):

        total = 0


        for category in self.categories.values():

            total += len(
                category["wishes"]
            )


        return total



    # ==================================================
    # RARITY
    # ==================================================

    def get_random_rarity(self):


        roll = random.randint(
            1,
            100
        )


        current = 0


        for rarity, data in self.rarities.items():


            current += data.get(
                "chance",
                0
            )


            if roll <= current:

                return rarity



        return "common"



    def get_rarity_info(
        self,
        rarity
    ):


        return self.rarities.get(
            rarity,
            {
                "name": rarity,
                "chance": 0
            }
        )




    # ==================================================
    # RANDOM WISH
    # ==================================================

    def get_random_wish(self):


        if not self.categories:

            return None



        rarity = self.get_random_rarity()



        available = []



        for category, data in self.categories.items():


            if data["rarity"] == rarity:


                for wish in data["wishes"]:

                    available.append({

                        "category": category,

                        "category_name":
                            data["name"],

                        "text":
                            wish,

                        "image":
                            data["image"],

                        "rarity":
                            rarity

                    })




        if not available:


            for category, data in self.categories.items():


                for wish in data["wishes"]:

                    available.append({

                        "category": category,

                        "category_name":
                            data["name"],

                        "text":
                            wish,

                        "image":
                            data["image"],

                        "rarity":
                            data["rarity"]

                    })




        if not available:

            return None



        result = random.choice(
            available
        )



        rarity_info = self.get_rarity_info(
            result["rarity"]
        )



        result["rarity_name"] = rarity_info.get(
            "name",
            result["rarity"]
        )


        return result




    # ==================================================
    # USER
    # ==================================================

    def get_user(
        self,
        user_id
    ):


        user_id = str(
            user_id
        )


        if user_id not in self.users:


            self.users[user_id] = {

                "count": 0,

                "last_wish": None,

                "last_time": None

            }


        return self.users[user_id]




    # ==================================================
    # COOLDOWN
    # ==================================================

    def can_receive(
        self,
        user_id
    ):


        user = self.get_user(
            user_id
        )


        if not user["last_time"]:

            return True



        last = datetime.fromisoformat(
            user["last_time"]
        )


        return datetime.now() >= (

            last +

            timedelta(
                minutes=self.cooldown_minutes
            )

        )




    def cooldown_left(
        self,
        user_id
    ):


        user = self.get_user(
            user_id
        )


        if not user["last_time"]:

            return 0



        last = datetime.fromisoformat(
            user["last_time"]
        )


        end = last + timedelta(
            minutes=self.cooldown_minutes
        )


        seconds = (
            end - datetime.now()
        ).total_seconds()


        return max(
            0,
            int(seconds)
        )




    # ==================================================
    # GIVE
    # ==================================================

    def give_wish(
        self,
        user_id
    ):


        if not self.can_receive(
            user_id
        ):


            return {

                "success": False,

                "cooldown":
                    self.cooldown_left(
                        user_id
                    )

            }



        wish = self.get_random_wish()



        if not wish:


            return {

                "success": False,

                "cooldown": 0

            }



        user = self.get_user(
            user_id
        )


        user["count"] += 1

        user["last_wish"] = wish

        user["last_time"] = datetime.now().isoformat()



        return {

            "success": True,

            "wish": wish,

            "cooldown": 0

        }



    # ==================================================
    # STATS
    # ==================================================

    def get_user_stats(
        self,
        user_id
    ):

        return self.get_user(
            user_id
        )