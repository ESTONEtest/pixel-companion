import discord


class BattleEmbedSystem:

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
    # FORMAT LOG
    # ==================================================

    def format_log(
        self,
        log: list,
        limit: int = 10
    ):

        if not log:
            return "Нет записей."

        selected_log = log[-limit:]

        text = "\n".join(
            selected_log
        )

        if len(log) > limit:

            text = (
                f"Показаны последние **{limit}** действий.\n"
                f"{text}"
            )

        if len(text) > 1000:

            text = text[-1000:]

        return text

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
    # DEFEAT EMBED
    # ==================================================

    def defeat(
        self,
        result
    ):

        embed = discord.Embed(
            title="💀 Поражение",
            description=f"Вы проиграли бой против **{result.monster_name}**.",
            color=discord.Color.red()
        )

        embed.add_field(
            name="👹 Противник",
            value=result.monster_name,
            inline=False
        )

        embed.add_field(
            name="❤️ Ваш HP",
            value=f"**{result.player_hp}**",
            inline=True
        )

        embed.add_field(
            name="🩸 HP монстра",
            value=f"**{result.monster_hp}**",
            inline=True
        )

        embed.add_field(
            name="📜 Ход боя",
            value=self.format_log(
                result.log
            ),
            inline=False
        )

        embed.set_footer(
            text="Восстановите здоровье и попробуйте снова."
        )

        return embed

    # ==================================================
    # VICTORY EMBED
    # ==================================================

    def victory(
        self,
        result
    ):

        embed = discord.Embed(
            title="🏆 Победа!",
            description=f"Вы одолели **{result.monster_name}**.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="👹 Противник",
            value=result.monster_name,
            inline=False
        )

        embed.add_field(
            name="❤️ Ваш HP",
            value=f"**{result.player_hp}**",
            inline=True
        )

        embed.add_field(
            name="🩸 HP монстра",
            value=f"**{result.monster_hp}**",
            inline=True
        )

        embed.add_field(
            name="✨ Опыт",
            value=f"**+{result.xp} XP**",
            inline=True
        )

        embed.add_field(
            name="🪙 Монеты",
            value=f"**+{result.coins}**",
            inline=True
        )

        embed.add_field(
            name="🎁 Добыча",
            value=self.format_loot(
                result.loot
            ),
            inline=False
        )

        embed.add_field(
            name="📜 Ход боя",
            value=self.format_log(
                result.log
            ),
            inline=False
        )

        embed.set_footer(
            text="Награда добавлена к вашему персонажу."
        )

        return embed


battle_embed_system = BattleEmbedSystem()