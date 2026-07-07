import discord


LEVEL_ROLES = {

    1: {
        "name": "🌱 Rookie",
        "role_id": 1474282467237298318
    },

    5: {
        "name": "🕹 Player",
        "role_id": 1523486181243748402
    },

    10: {
        "name": "🎮 Gamer",
        "role_id": 1523486189351342282
    },

    20: {
        "name": "⚔ Veteran",
        "role_id": 1523486191989690368
    },

    35: {
        "name": "💎 Elite",
        "role_id": 1523486196037189782
    },

    50: {
        "name": "🔥 Pro Player",
        "role_id": 1523488555413012611
    },

    75: {
        "name": "👑 Legend",
        "role_id": 1523488560139862186
    }

}



class RoleManager:


    def get_role(
        self,
        level: int
    ):

        current_role = None


        for lvl, data in sorted(LEVEL_ROLES.items()):

            if level >= lvl:
                current_role = data


        return current_role



    async def update_role(
        self,
        member: discord.Member,
        level: int
    ):

        role_data = self.get_role(level)


        if not role_data:
            return


        role = member.guild.get_role(
            role_data["role_id"]
        )


        if not role:
            return


        rank_roles = [
            data["role_id"]
            for data in LEVEL_ROLES.values()
        ]


        remove_roles = []


        for old_role in member.roles:

            if old_role.id in rank_roles:
                remove_roles.append(old_role)


        if remove_roles:

            await member.remove_roles(
                *remove_roles
            )


        if role not in member.roles:

            await member.add_roles(
                role
            )


role_manager = RoleManager()