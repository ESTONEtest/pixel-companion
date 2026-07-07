import aiohttp


class TwitchChecker:


    def __init__(self):

        self.url = (
            "https://www.twitch.tv/"
            "captain_icecream"
        )



    async def is_live(self):

        try:

            headers = {
                "User-Agent":
                "Mozilla/5.0"
            }


            async with aiohttp.ClientSession() as session:

                async with session.get(
                    self.url,
                    headers=headers
                ) as response:


                    text = await response.text()



                    if (
                        "isLiveBroadcast" in text
                        or
                        '"isLive":true' in text
                    ):

                        return True



            return False


        except Exception:

            return False



twitch_checker = TwitchChecker()