import discord
from discord.ext import commands

from managers.role_manager import role_manager


class TestRoles(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    @commands.command(
        name="testroles"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def testroles(
        self,
        ctx
    ):


        guild = ctx.guild
        member = ctx.author


        levels = [
            1,
            5,
            10,
            20,
            35,
            50,
            75
        ]


        result = []


        for level in levels:


            role_data = role_manager.get_role(
                level
            )


            if not role_data:

                result.append(
                    f"❌ Level {level} - нет роли"
                )

                continue



            role = guild.get_role(
                role_data["role_id"]
            )


            if role:

                result.append(
                    f"✅ Level {level} → {role.mention}"
                )

            else:

                result.append(
                    f"❌ Level {level} → роль не найдена"
                )



        embed = discord.Embed(
            title="🎭 ROLE SYSTEM TEST",
            description="\n".join(result),
            color=0x5865F2
        )


        await ctx.send(
            embed=embed
        )



async def setup(bot):

    print(
        "✅ TEST ROLES COG LOADED"
    )


    await bot.add_cog(
        TestRoles(bot)
    )