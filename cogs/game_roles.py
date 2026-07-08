import discord

from discord.ext import commands

from config import (
    GAME_ROLE_CHANNEL_ID,
    GAME_ROLES
)


class GameRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = None


    @commands.Cog.listener()
    async def on_ready(self):

        channel = self.bot.get_channel(
            GAME_ROLE_CHANNEL_ID
        )

        if channel is None:
            return


        # ищем уже созданное сообщение
        async for message in channel.history(limit=20):

            if message.author == self.bot.user:
                self.role_message_id = message.id
                return


        embed = discord.Embed(
            title="🎮 ИГРОВЫЕ РОЛИ",
            description=(
                "⚔️ **Выберите свою игровую специализацию!**\n\n"
                "Получите роль своей любимой игры "
                "и находите игроков с похожими интересами.\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "⛏️ **Minecraft**\n"
                "Строители, исследователи и любители приключений.\n\n"

                "🔥 **Souls**\n"
                "Воины Elden Ring, Dark Souls и других Souls-like миров.\n\n"

                "🎯 **CS2**\n"
                "Игроки соревновательной арены и тактики.\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "✨ Нажмите на реакцию ниже, чтобы получить роль!"
            ),
            color=0x5865F2
        )


        message = await channel.send(
            embed=embed
        )

        self.role_message_id = message.id


        for emoji in GAME_ROLES.keys():

            await message.add_reaction(
                emoji
            )


    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        payload
    ):

        if payload.channel_id != GAME_ROLE_CHANNEL_ID:
            return


        if payload.user_id == self.bot.user.id:
            return


        if payload.message_id != self.role_message_id:
            return


        emoji = str(payload.emoji)


        if emoji not in GAME_ROLES:
            return


        guild = self.bot.get_guild(
            payload.guild_id
        )

        member = guild.get_member(
            payload.user_id
        )


        role = guild.get_role(
            GAME_ROLES[emoji]
        )


        if role:

            await member.add_roles(
                role
            )


    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self,
        payload
    ):

        if payload.channel_id != GAME_ROLE_CHANNEL_ID:
            return


        if payload.message_id != self.role_message_id:
            return


        emoji = str(payload.emoji)


        if emoji not in GAME_ROLES:
            return


        guild = self.bot.get_guild(
            payload.guild_id
        )

        member = guild.get_member(
            payload.user_id
        )


        role = guild.get_role(
            GAME_ROLES[emoji]
        )


        if role:

            await member.remove_roles(
                role
            )



async def setup(bot):

    await bot.add_cog(
        GameRoles(bot)
    )