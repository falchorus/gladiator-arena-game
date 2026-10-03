import random
import os
import time
import sys

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header(title):
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)

class Weapon:
    def __init__(self, name, min_dmg, max_dmg, cost, crit_bonus=0, speed=0):
        self.name = name
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.cost = cost
        self.crit_bonus = crit_bonus
        self.speed = speed

class Armor:
    def __init__(self, name, defense, cost, speed_penalty=0):
        self.name = name
        self.defense = defense
        self.cost = cost
        self.speed_penalty = speed_penalty

WEAPONS = [
    Weapon("Bare Fists", 2, 5, 0, crit_bonus=5, speed=5),
    Weapon("Wooden Rudis", 4, 8, 30, crit_bonus=5, speed=2),
    Weapon("Bronze Pugio (Dagger)", 5, 12, 75, crit_bonus=15, speed=4),
    Weapon("Iron Gladius (Shortsword)", 10, 18, 150, crit_bonus=10, speed=1),
    Weapon("Sica (Curved Sword)", 12, 22, 250, crit_bonus=12, speed=0),
    Weapon("Trident & Net", 14, 28, 400, crit_bonus=8, speed=3),
    Weapon("Spatha (Longsword)", 18, 34, 600, crit_bonus=10, speed=-1),
    Weapon("Executioner's Greataxe", 25, 45, 900, crit_bonus=20, speed=-3),
]

ARMORS = [
    Armor("Rags", 0, 0, 0),
    Armor("Leather Subligaculum", 3, 40, 0),
    Armor("Hardened Leather Lorica", 7, 120, 1),
    Armor("Bronze Galerus & Manica", 12, 250, 2),
    Armor("Iron Lorica Hamata (Chainmail)", 18, 450, 3),
    Armor("Gladiator Segmentata (Plate)", 26, 750, 5),
]

CLASSES = {
    "1": {"name": "Murmillo", "hp": 110, "str": 12, "agi": 8, "desc": "Heavy defender with high health and resilience."},
    "2": {"name": "Retiarius", "hp": 85, "str": 9, "agi": 14, "desc": "Agile skirmisher with high speed and critical strike chance."},
    "3": {"name": "Thraex", "hp": 95, "str": 11, "agi": 11, "desc": "Balanced fighter skilled with curved blades and quick strikes."}
}

ENEMY_NAMES = ["Strikus", "Decimus", "Varo", "Brutus", "Gannicus", "Crixus", "Spartacus", "Flamma", "Verus", "Priscus"]

class Fighter:
    def __init__(self, name, hp, strength, agility, weapon, armor, is_player=False):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.strength = strength
        self.agility = agility
        self.weapon = weapon
        self.armor = armor
        self.is_player = is_player
        self.wins = 0
        self.gold = 50
        self.fame = 0

    @property
    def speed(self):
        return max(1, self.agility + self.weapon.speed - self.armor.speed_penalty)

    @property
    def defense(self):
        return self.armor.defense + (self.strength // 3)

    def is_alive(self):
        return self.hp > 0

    def calculate_damage(self, attack_type):
        base_dmg = random.randint(self.weapon.min_dmg, self.weapon.max_dmg) + (self.strength // 2)
        multiplier = 1.0
        crit_chance = 5 + self.agility + self.weapon.crit_bonus

        if attack_type == "heavy":
            multiplier = 1.5
            crit_chance -= 5
        elif attack_type == "quick":
            multiplier = 0.75
            crit_chance += 10
        elif attack_type == "taunt":
            return 0, False

        is_crit = random.randint(1, 100) <= crit_chance
        if is_crit:
            multiplier *= 1.75

        damage = max(1, int(base_dmg * multiplier))
        return damage, is_crit

class GladiatorArena:
    def __init__(self):
        self.player = None
        self.day = 1
        self.crowd_favor = 50  # 0 to 100

    def create_character(self):
        clear()
        print_header("THE AMPHITHEATER - CHARACTER CREATION")
        name = input("Enter your Gladiator's Name: ").strip() or "Spartacus"

        print("\nChoose your Fighting Style:")
        for key, c in CLASSES.items():
            print(f"[{key}] {c['name']:<12} HP: {c['hp']:<4} STR: {c['str']:<4} AGI: {c['agi']:<4} | {c['desc']}")

        choice = ""
        while choice not in CLASSES:
            choice = input("\nSelect Class (1-3): ").strip()

        cls = CLASSES[choice]
        self.player = Fighter(
            name=name,
            hp=cls["hp"],
            strength=cls["str"],
            agility=cls["agi"],
            weapon=WEAPONS[0],
            armor=ARMORS[0],
            is_player=True
        )
        print(f"\nWelcome to the Sands, {self.player.name} the {cls['name']}!")
        time.sleep(1.5)

    def main_menu(self):
        while self.player.is_alive():
            clear()
            print_header(f"LUDUS GROUNDS - DAY {self.day}")
            print(f"Gladiator : {self.player.name}")
            print(f"Health    : {self.player.hp}/{self.player.max_hp}")
            print(f"Stats     : STR {self.player.strength} | AGI {self.player.agility} | SPD {self.player.speed} | DEF {self.player.defense}")
            print(f"Equipment : Weapon: {self.player.weapon.name} | Armor: {self.player.armor.name}")
            print(f"Purse     : {self.player.gold} Gold | Fame: {self.player.fame} | Wins: {self.player.wins}")
            print("-" * 60)
            print("[1] Enter the Arena (Fight)")
            print("[2] Visit the Armory (Shop)")
            print("[3] Train Physical Stats")
            print("[4] Rest & Recover HP (Cost: 15 Gold)")
            print("[5] Retire in Glory (Quit)")
            print("=" * 60)

            choice = input("Select Option: ").strip()
            if choice == "1":
                self.start_arena_fight()
            elif choice == "2":
                self.shop()
            elif choice == "3":
                self.train()
            elif choice == "4":
                self.rest()
            elif choice == "5":
                print("\nYou step away from the blood and sand, retiring as a legend!")
                sys.exit()

    def shop(self):
        while True:
            clear()
            print_header("THE BLACKSMITH & ARMORY")
            print(f"Your Gold: {self.player.gold}")
            print("-" * 60)
            print("WEAPONS:")
            for i, w in enumerate(WEAPONS[1:], 1):
                owned = " (Equipped)" if self.player.weapon == w else ""
                print(f" [W{i}] {w.name:<24} Cost: {w.cost:<4} Dmg: {w.min_dmg}-{w.max_dmg:<3} Crit: +{w.crit_bonus}%{owned}")
            print("-" * 60)
            print("ARMOR:")
            for i, a in enumerate(ARMORS[1:], 1):
                owned = " (Equipped)" if self.player.armor == a else ""
                print(f" [A{i}] {a.name:<24} Cost: {a.cost:<4} Def: +{a.defense:<3} Spd Pen: -{a.speed_penalty}{owned}")
            print("-" * 60)
            print("[B] Back to Ludus")

            cmd = input("\nEnter item code to buy (e.g. W1 or A2): ").strip().upper()
            if cmd == "B":
                break

            if cmd.startswith("W") and cmd[1:].isdigit():
                idx = int(cmd[1:]) - 1
                if 0 <= idx < len(WEAPONS) - 1:
                    w = WEAPONS[idx + 1]
                    if self.player.gold >= w.cost:
                        self.player.gold -= w.cost
                        self.player.weapon = w
                        print(f"Purchased and equipped {w.name}!")
                    else:
                        print("Not enough gold!")
            elif cmd.startswith("A") and cmd[1:].isdigit():
                idx = int(cmd[1:]) - 1
                if 0 <= idx < len(ARMORS) - 1:
                    a = ARMORS[idx + 1]
                    if self.player.gold >= a.cost:
                        self.player.gold -= a.cost
                        self.player.armor = a
                        print(f"Purchased and equipped {a.name}!")
                    else:
                        print("Not enough gold!")
            time.sleep(1)

    def train(self):
        clear()
        print_header("TRAINING GROUNDS")
        cost = 25 + (self.player.wins * 10)
        print(f"Your Gold: {self.player.gold}")
        print(f"Training Cost: {cost} Gold per session\n")
        print("[1] Heavy Lifting (+2 Strength)")
        print("[2] Agility & Reflex Drills (+2 Agility)")
        print("[3] Endurance Conditioning (+10 Max HP)")
        print("[B] Back")

        choice = input("\nSelect training: ").strip().upper()
        if choice == "B":
            return

        if self.player.gold < cost:
            print("\nYou don't have enough gold to pay the Lanista!")
            time.sleep(1.2)
            return

        self.player.gold -= cost
        if choice == "1":
            self.player.strength += 2
            print("\nYour muscles grow denser! Strength increased by 2.")
        elif choice == "2":
            self.player.agility += 2
            print("\nYour footwork quickens! Agility increased by 2.")
        elif choice == "3":
            self.player.max_hp += 10
            self.player.hp += 10
            print("\nYour vital capacity expands! Max HP increased by 10.")
        self.day += 1
        time.sleep(1.5)

    def rest(self):
        if self.player.gold < 15:
            print("\nNot enough gold to purchase medicinal salve and rest!")
            time.sleep(1.2)
            return
        if self.player.hp >= self.player.max_hp:
            print("\nYou are already at full health!")
            time.sleep(1.2)
            return

        self.player.gold -= 15
        recovered = int(self.player.max_hp * 0.50)
        self.player.hp = min(self.player.max_hp, self.player.hp + recovered)
        self.day += 1
        print(f"\nYou rest and recover {recovered} HP. Current HP: {self.player.hp}/{self.player.max_hp}")
        time.sleep(1.5)

    def generate_enemy(self):
        scaling = self.player.wins
        name = random.choice(ENEMY_NAMES) + f" the {'Brute' if scaling % 2 == 0 else 'Slayer'}"
        hp = 60 + (scaling * 18)
        strength = 8 + (scaling * 2)
        agility = 6 + (scaling * 2)

        # Assign weapon/armor based on progression
        w_idx = min(len(WEAPONS) - 1, 1 + (scaling // 2))
        a_idx = min(len(ARMORS) - 1, (scaling // 2))

        return Fighter(name, hp, strength, agility, WEAPONS[w_idx], ARMORS[a_idx])

    def start_arena_fight(self):
        enemy = self.generate_enemy()
        self.crowd_favor = 50
        clear()
        print_header("BLOOD AND SAND - COMBAT ENTERED")
        print(f"The gates open! Step forth, {self.player.name}!")
        print(f"Opponent: {enemy.name}")
        print(f"Enemy Stats -> HP: {enemy.hp} | Weapon: {enemy.weapon.name} | Armor: {enemy.armor.name}")
        print("-" * 60)
        input("Press ENTER to clash steel...")

        while self.player.is_alive() and enemy.is_alive():
            clear()
            print_header(f"ARENA MATCH | CROWD FAVOR: {self.crowd_favor}%")
            print(f"YOU   : {self.player.name:<18} HP: {self.player.hp:<4}/{self.player.max_hp}")
            print(f"ENEMY : {enemy.name:<18} HP: {enemy.hp:<4}/{enemy.max_hp}")
            print("-" * 60)
            print("[1] Standard Attack  (Normal Dmg & Precision)")
            print("[2] Heavy Swing      (+50% Dmg, Lower Accuracy)")
            print("[3] Quick Thrust     (-25% Dmg, High Speed & Crit)")
            print("[4] Taunt Crowd      (Gain Crowd Favor & Bonus Dmg Next Turn)")
            print("[5] Defensive Guard  (Reduce Incoming Damage by 50%)")
            print("=" * 60)

            p_guarded = False
            p_action = input("Choose Combat Action: ").strip()

            # Determine initiative
            p_first = self.player.speed >= enemy.speed or random.randint(1, 100) <= 50

            # Player Action Execution
            if p_action == "1":
                dmg, crit = self.player.calculate_damage("standard")
                self.apply_attack(self.player, enemy, dmg, crit, "Standard Attack")
            elif p_action == "2":
                dmg, crit = self.player.calculate_damage("heavy")
                self.apply_attack(self.player, enemy, dmg, crit, "Heavy Swing")
            elif p_action == "3":
                dmg, crit = self.player.calculate_damage("quick")
                self.apply_attack(self.player, enemy, dmg, crit, "Quick Thrust")
            elif p_action == "4":
                self.crowd_favor = min(100, self.crowd_favor + 20)
                print(f"\nYou raise your arms! The crowd cheers wildly! (+20% Favor)")
                time.sleep(1)
            elif p_action == "5":
                p_guarded = True
                print("\nYou raise your guard, preparing to absorb incoming strikes!")
                time.sleep(1)

            if not enemy.is_alive():
                break

            # Enemy AI Turn
            e_action = random.choice(["standard", "heavy", "quick"])
            e_dmg, e_crit = enemy.calculate_damage(e_action)

            # Apply player guard
            if p_guarded:
                e_dmg = e_dmg // 2

            self.apply_attack(enemy, self.player, e_dmg, e_crit, f"Enemy {e_action.capitalize()}")

            input("\nPress ENTER for next round...")

        # Combat Outcome
        if self.player.is_alive():
            gold_reward = 40 + (self.player.wins * 25) + (self.crowd_favor // 2)
            fame_reward = 10 + (self.crowd_favor // 5)
            self.player.wins += 1
            self.player.gold += gold_reward
            self.player.fame += fame_reward
            self.day += 1

            print_header("VICTORY IN THE ARENA!")
            print(f"You slain {enemy.name}!")
            print(f"Earned: {gold_reward} Gold | +{fame_reward} Fame")
            time.sleep(2.5)
        else:
            print_header("DEFEAT AND DEATH")
            print(f"You fell on the arena floor... {enemy.name} stands victorious.")
            print(f"Final Record: {self.player.wins} Wins | {self.player.fame} Fame")
            sys.exit()

    def apply_attack(self, attacker, defender, damage, is_crit, action_name):
        hit_chance = 75 + (attacker.speed - defender.speed) * 3
        hit_chance = max(35, min(95, hit_chance))

        if random.randint(1, 100) <= hit_chance:
            actual_dmg = max(1, damage - defender.defense)
            defender.hp -= actual_dmg
            crit_str = " *** CRITICAL HIT! ***" if is_crit else ""
            print(f"\n{attacker.name} uses {action_name} dealing {actual_dmg} damage to {defender.name}!{crit_str}")
            if attacker.is_player:
                self.crowd_favor = min(100, self.crowd_favor + (5 if is_crit else 2))
        else:
            print(f"\n{attacker.name}'s {action_name} MISSED {defender.name}!")

if __name__ == "__main__":
    game = GladiatorArena()
    game.create_character()
    game.main_menu()