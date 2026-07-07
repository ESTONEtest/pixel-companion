from systems.damage import damage_system
from systems.critical import critical_system


class CombatSystem:

    # ==================================================
    # PLAYER ATTACK
    # ==================================================

    def player_attack(
        self,
        player,
        monster
    ):

        critical = critical_system.is_critical(
            player["luck"]
        )

        damage = damage_system.calculate_damage(
            attack=player["attack"],
            defense=monster.get("defense", 0),
            bonus=10,
            critical=critical
        )

        monster["hp"] = max(
            0,
            monster["hp"] - damage
        )

        return {
            "damage": damage,
            "critical": critical,
            "hp": monster["hp"]
        }

    # ==================================================
    # MONSTER ATTACK
    # ==================================================

    def monster_attack(
        self,
        monster,
        player
    ):

        damage = damage_system.calculate_damage(
            attack=monster["attack"],
            defense=player["defense"],
            bonus=5
        )

        player["hp"] = max(
            0,
            player["hp"] - damage
        )

        return {
            "damage": damage,
            "hp": player["hp"]
        }


combat_system = CombatSystem()