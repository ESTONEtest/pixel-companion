from discord.ext import commands

from managers.player_manager import player_manager
from managers.monster_manager import monster_manager
from managers.inventory_manager import inventory_manager

from systems.combat import combat_system
from systems.battle_embed import battle_embed_system


class Battle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ==================================================
    # FIGHT
    # ==================================================

    @commands.command(name="fight")
    async def fight(self, ctx):

        user_id = ctx.author.id

        player = player_manager.get_player(
            user_id
        )

        if not player:

            player_manager.create_player(
                user_id,
                ctx.author.name
            )

            player = player_manager.get_player(
                user_id
            )

        if not player:

            await ctx.send(
                "❌ Не удалось создать персонажа. Попробуйте еще раз."
            )

            return

        if player["hp"] <= 0:

            await ctx.send(
                "❤️ У вас нет здоровья. Используйте восстановление."
            )

            return

        monster = monster_manager.get_random_monster_for_player(
            player
        )

        if not monster:

            await ctx.send(
                "❌ Не удалось найти монстра для боя."
            )

            return

        monster.setdefault(
            "name",
            "Неизвестный монстр"
        )

        monster.setdefault(
            "defense",
            0
        )

        battle_player = {

            "hp": player["hp"],
            "max_hp": player["max_hp"],

            "attack": player["attack"],
            "defense": player["defense"],
            "luck": player["luck"]

        }

        result = combat_system.start_battle(
            user_id,
            battle_player,
            monster
        )

        if result.victory and result.loot:

            inventory_manager.add_item(
                user_id,
                result.loot,
                1
            )

        if result.victory:

            embed = battle_embed_system.victory(
                result
            )

        else:

            embed = battle_embed_system.defeat(
                result
            )

        await ctx.send(
            embed=embed
        )


async def setup(bot):

    print("✅ BATTLE COG LOADED")

    await bot.add_cog(
        Battle(bot)
    )