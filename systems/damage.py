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

        damage = random.randint(
            attack,
            attack + bonus
        )

        damage -= defense

        damage = max(1, damage)

        if critical:
            damage *= 2

        return damage


damage_system = DamageSystem()