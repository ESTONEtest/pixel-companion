class HealingSystem:

    # ==================================================
    # HEAL
    # ==================================================

    def heal(
        self,
        current_hp: int,
        amount: int,
        max_hp: int
    ) -> int:

        current_hp = max(
            0,
            current_hp
        )

        amount = max(
            0,
            amount
        )

        max_hp = max(
            1,
            max_hp
        )

        return min(
            current_hp + amount,
            max_hp
        )


healing_system = HealingSystem()