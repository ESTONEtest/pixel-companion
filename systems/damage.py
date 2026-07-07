import random


class DamageSystem:

    # ==================================================
    # UNIVERSAL DAMAGE
    # ==================================================

    def calculate_damage(
        self,
        attack: int,
        defense: int = 0,
        bonus: int = 10,
        critical: bool = False
    ) -> int:

        attack = max(
            1,
            attack
        )

        defense = max(
            0,
            defense
        )

        bonus = max(
            0,
            bonus
        )

        damage = random.randint(
            attack,
            attack + bonus
        )

        damage -= defense

        damage = max(
            1,
            damage
        )

        if critical:

            damage *= 2

        return damage


damage_system = DamageSystem()