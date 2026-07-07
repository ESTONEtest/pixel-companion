from dataclasses import dataclass, field

from managers.player_manager import player_manager
from systems.damage import damage_system
from systems.critical import critical_system
from systems.loot_drop import loot_drop_system
from systems.battle_log import battle_log_system


# ==================================================
# RESULT
# ==================================================

@dataclass
class BattleResult:

    victory: bool = False

    monster_name: str = ""

    xp: int = 0

    coins: int = 0

    loot: str | None = None

    player_hp: int = 0

    monster_hp: int = 0

    log: list = field(default_factory=list)


# ==================================================
# BATTLE
# ==================================================

class Battle:

    def __init__(
        self,
        user_id: int,
        player: dict,
        monster: dict
    ):

        self.user_id = user_id

        self.player = {

            "hp": player["hp"],
            "max_hp": player["max_hp"],

            "attack": player["attack"],
            "defense": player["defense"],
            "luck": player["luck"]
        }

        self.monster = monster.copy()

        self.monster.setdefault(
            "defense",
            0
        )

        self.log = []

        self.finished = False

        self.result = BattleResult()

    # ==================================================
    # PLAYER TURN
    # ==================================================

    def player_attack(self):

        critical = critical_system.is_critical(
            self.player["luck"]
        )

        damage = damage_system.calculate_damage(
            attack=self.player["attack"],
            defense=self.monster["defense"],
            bonus=10,
            critical=critical
        )

        self.monster["hp"] = max(
            0,
            self.monster["hp"] - damage
        )

        if critical:

            self.log.append(
                battle_log_system.player_critical(
                    damage
                )
            )

        else:

            self.log.append(
                battle_log_system.player_attack(
                    damage
                )
            )

        return damage

    # ==================================================
    # MONSTER TURN
    # ==================================================

    def monster_attack(self):

        damage = damage_system.calculate_damage(
            attack=self.monster["attack"],
            defense=self.player["defense"],
            bonus=5
        )

        self.player["hp"] = max(
            0,
            self.player["hp"] - damage
        )

        self.log.append(
            battle_log_system.monster_attack(
                self.monster["name"],
                damage
            )
        )

        return damage

    # ==================================================
    # HEAL
    # ==================================================

    def heal(self, amount: int = 25):

        old_hp = self.player["hp"]

        self.player["hp"] = min(
            self.player["max_hp"],
            self.player["hp"] + amount
        )

        healed = self.player["hp"] - old_hp

        self.log.append(
            battle_log_system.heal(
                healed
            )
        )

        return healed

    # ==================================================
    # DEFEND
    # ==================================================

    def defend(self):

        self.player["defense"] += 10

        self.log.append(
            battle_log_system.defend()
        )

    # ==================================================
    # RUN
    # ==================================================

    def run(self):

        self.finished = True

        self.result.victory = False

        self.log.append(
            battle_log_system.run()
        )

    # ==================================================
    # CHECK
    # ==================================================

    def is_finished(self):

        if self.player["hp"] <= 0:
            return True

        if self.monster["hp"] <= 0:
            return True

        return self.finished

    # ==================================================
    # WINNER
    # ==================================================

    def winner(self):

        if self.monster["hp"] <= 0:
            return "player"

        if self.player["hp"] <= 0:
            return "monster"

        return None

    # ==================================================
    # START
    # ==================================================

    def start(self):

        self.log.append(
            battle_log_system.start(
                self.monster["name"]
            )
        )

        while not self.is_finished():

            self.player_attack()

            if self.is_finished():
                break

            self.monster_attack()

        self.result.player_hp = self.player["hp"]

        self.result.monster_hp = self.monster["hp"]

        self.result.monster_name = self.monster["name"]

        self.result.log = self.log.copy()

        return self.result


# ==================================================
# COMBAT SYSTEM
# ==================================================

class CombatSystem:

    def start_battle(
        self,
        user_id: int,
        player: dict,
        monster: dict
    ):

        battle = Battle(
            user_id=user_id,
            player=player,
            monster=monster
        )

        result = battle.start()

        player_manager.set_hp(
            user_id,
            result.player_hp
        )

        # ==========================
        # DEFEAT / ESCAPE
        # ==========================

        if result.monster_hp > 0:

            result.log.append(
                battle_log_system.defeat()
            )

            return result

        # ==========================
        # VICTORY
        # ==========================

        result.victory = True

        result.xp = monster["reward_xp"]

        result.coins = monster["reward_coins"]

        player_manager.add_xp(
            user_id,
            result.xp
        )

        player_manager.add_coins(
            user_id,
            result.coins
        )

        player_manager.add_monster_kill(
            user_id
        )

        loot = loot_drop_system.roll_loot()

        result.loot = loot

        result.log.append(
            battle_log_system.victory(
                result.monster_name
            )
        )

        result.log.append(
            battle_log_system.reward_xp(
                result.xp
            )
        )

        result.log.append(
            battle_log_system.reward_coins(
                result.coins
            )
        )

        result.log.append(
            battle_log_system.loot(
                result.loot
            )
        )

        return result


combat_system = CombatSystem()