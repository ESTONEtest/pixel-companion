import discord
from discord.ext import commands

VOICE_CATEGORY_NAME = "🎧 Pixel Voices"
TRIGGER_CHANNEL_NAME = "➕ create-voice"


class VoiceSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ─────────────────────────────
    # CREATE VOICE
    # ─────────────────────────────
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # вход в триггер
        if after.channel and after.channel.name == TRIGGER_CHANNEL_NAME:

            guild = member.guild

            category = discord.utils.get(guild.categories, name=VOICE_CATEGORY_NAME)
            if category is None:
                category = await guild.create_category(VOICE_CATEGORY_NAME)

            voice_channel = await guild.create_voice_channel(
                name=f"🎮 {member.display_name}",
                category=category
            )

            await member.move_to(voice_channel)

            # добавляем панель управления
            await self.send_panel(voice_channel, member)

        # авто удаление
        if before.channel and before.channel.name != TRIGGER_CHANNEL_NAME:
            if len(before.channel.members) == 0:
                try:
                    await before.channel.delete()
                except:
                    pass

    # ─────────────────────────────
    # VOICE CONTROL PANEL
    # ─────────────────────────────
    async def send_panel(self, channel, owner):

        embed = discord.Embed(
            title="🎧 Voice Panel",
            description="Управление твоей комнатой",
            color=0x8A2BE2
        )

        embed.add_field(
            name="🎮 Команды",
            value=(
                "🔒 lock — закрыть комнату\n"
                "🔓 unlock — открыть комнату\n"
                "✏️ rename — изменить название\n"
                "👢 kick — выгнать участника"
            ),
            inline=False
        )

        await channel.send(content=owner.mention, embed=embed)


    # ─────────────────────────────
    # TEXT COMMANDS (inside voice category)
    # ─────────────────────────────
    @commands.command()
    async def lock(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.set_permissions(ctx.guild.default_role, connect=False)
            await ctx.send("🔒 Комната закрыта")

    @commands.command()
    async def unlock(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.set_permissions(ctx.guild.default_role, connect=True)
            await ctx.send("🔓 Комната открыта")

    @commands.command()
    async def rename(self, ctx, *, name):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.edit(name=name)
            await ctx.send(f"✏️ Новое имя: {name}")

    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if member.voice and member.voice.channel == channel:
                await member.move_to(None)
                await ctx.send(f"👢 {member.name} кикнут")


async def setup(bot):
    await bot.add_cog(VoiceSystem(bot))