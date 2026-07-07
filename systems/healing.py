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

        return min(current_hp + amount, max_hp)


healing_system = HealingSystem()