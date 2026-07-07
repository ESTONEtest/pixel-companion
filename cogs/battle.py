import discord

from discord.ext import commands

from managers.player_manager import player_manager
from managers.monster_manager import monster_manager
from managers.inventory_manager import inventory_manager

from systems.combat import combat_system
from systems.loot_drop import loot_drop_system


class Battle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # ==================================================
    # FIGHT
    # ==================================================

    @commands.command(name="fight")
    async def fight(self, ctx):

        user_id = ctx.author.id


        # Получаем игрока

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


        # Создаем монстра

        monster = monster_manager.get_random_monster()


        # Добавляем недостающие параметры

        monster.setdefault(
            "defense",
            0
        )


        player_hp = player["hp"]


        if player_hp <= 0:

            await ctx.send(
                "❤️ У вас нет здоровья. Используйте восстановление."
            )

            return



        # Копия игрока для боя

        battle_player = {

            "hp": player["hp"],
            "attack": player["attack"],
            "defense": player["defense"],
            "luck": player["luck"]

        }



        log = []


        # ==================================================
        # BATTLE LOOP
        # ==================================================

        while True:


            # Игрок атакует

            player_attack = combat_system.player_attack(
                battle_player,
                monster
            )


            if player_attack["critical"]:

                log.append(
                    f"💥 Крит! Вы нанесли {player_attack['damage']} урона"
                )

            else:

                log.append(
                    f"⚔ Вы нанесли {player_attack['damage']} урона"
                )



            if monster["hp"] <= 0:

                break



            # Монстр атакует


            monster_attack = combat_system.monster_attack(
                monster,
                battle_player
            )


            log.append(
                f"👹 Монстр нанес {monster_attack['damage']} урона"
            )


            if battle_player["hp"] <= 0:

                break



        # ==================================================
        # DEFEAT
        # ==================================================

        if battle_player["hp"] <= 0:


            embed = discord.Embed(
                title="💀 Поражение",
                color=discord.Color.red()
            )


            embed.add_field(
                name="👹 Монстр",
                value=monster["name"]
            )


            embed.add_field(
                name="❤️ Ваш HP",
                value=f"{battle_player['hp']}"
            )


            await ctx.send(
                embed=embed
            )


            return



        # ==================================================
        # VICTORY
        # ==================================================


        player_manager.add_xp(
            user_id,
            monster["reward_xp"]
        )


        player_manager.add_coins(
            user_id,
            monster["reward_coins"]
        )



        loot = loot_drop_system.roll_loot()


        loot_text = "Нет"



        if loot:


            inventory_manager.add_item(
                user_id,
                loot,
                1
            )

            loot_text = loot



        embed = discord.Embed(
            title="⚔ Победа!",
            color=discord.Color.green()
        )


        embed.add_field(
            name="👹 Монстр",
            value=monster["name"],
            inline=False
        )


        embed.add_field(
            name="❤️ Ваш HP",
            value=f"{battle_player['hp']}",
            inline=True
        )


        embed.add_field(
            name="✨ XP",
            value=f"+{monster['reward_xp']}",
            inline=True
        )


        embed.add_field(
            name="💰 Coins",
            value=f"+{monster['reward_coins']}",
            inline=True
        )


        embed.add_field(
            name="🎁 Лут",
            value=loot_text,
            inline=False
        )


        embed.add_field(
            name="📜 Бой",
            value="\n".join(log[-10:]),
            inline=False
        )


        await ctx.send(
            embed=embed
        )



async def setup(bot):

    print("✅ BATTLE COG LOADED")

    await bot.add_cog(
        Battle(bot)
    )