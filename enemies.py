import random


def slime(level):
    slime_stats = {
        "str": (random.randint(1, 15) - 10) // 2 + (level - 1),
        "dex": (random.randint(1, 15) - 10) // 2 + (level - 1),
        "con": (random.randint(4, 15) - 10) // 2 + (level - 1),
        "wis": (random.randint(1, 15) - 10) // 2 + (level - 1),
        "int": (random.randint(1, 15) - 10) // 2 + (level - 1),
        "cha": (random.randint(1, 15) - 10) // 2 + (level - 1),
        "ac": 8 + random.randint(-1, 1)
        }
    slime_stats["health"] = max(random.randint(1, 5) + random.randint(1, 5) + slime_stats["con"] + 2, 1)
    modifier = ["lazy", "fabulous", "cringe", "random", "wild", "sad", "all-knowing", "playboy", "fishy", "green",
                "light green", "ugly", "eccentric"]
    random.shuffle(modifier)
    slime_stats["name"] = f'{modifier[1]} slime'
    return slime_stats


def d20():  # a basic d20 that also tells for critical fails/successes.
    d20_roll = random.randint(1, 20)
    if d20_roll == 1:
        print("Critical fail!")
        return d20_roll
    elif d20_roll == 20:
        print("Critical success!")
        return d20_roll
    else:
        return d20_roll


modifier = ["lazy", "fabulous", "cringe", "random", "wild", "sad", "all-knowing", "playboy", "fishy", "green",
            "light green", "ugly", "eccentric"]
random.shuffle(modifier)


class Monster:
    def __init__(self, name, lvl=1):
        self.lvl = lvl
        self.str = (random.randint(1, 15) - 10) // 2 + (lvl - 1)
        self.dex = (random.randint(1, 15) - 10) // 2 + (lvl - 1)
        self.con = (random.randint(1, 15) - 10) // 2 + (lvl - 1)
        self.wis = (random.randint(1, 15) - 10) // 2 + (lvl - 1)
        self.int = (random.randint(1, 15) - 10) // 2 + (lvl - 1)
        self.cha = (random.randint(1, 15) - 10) // 2 + (lvl - 1)
        self.ac = 8 + random.randint(-1, 1)
        self.health = max(random.randint(1, 5) + random.randint(1, 5) + self.con + 2, 1)
        self.name = modifier[1] + " " + name

    def basic_attack(self, status):
        d20roll = d20()
        attack_roll = d20roll + self.str - status["ac"]
        damage = max((random.randint(1, 6) + self.str), 1)
        if d20roll == 1:
            return status["health"], status["poison"]
        elif d20roll == 20:
            status["health"] -= damage
            print(f"{damage} damage!")
            return status["health"], status["poison"]
        elif attack_roll > 0:
            status["health"] -= damage
            print(f"{damage} damage!")
            return status["health"], status["poison"]
        else:
            print("Miss!")
            return status["health"], status["poison"]

    def poison(self, status):
        d20roll = d20()
        attack_roll = d20roll + self.str - status["ac"]
        damage = max((random.randint(1, 2) + self.str), 1)
        if d20roll == 1:
            return status["health"], status["poison"]
        elif d20roll == 20:
            status["health"] -= damage
            print(f"{damage} damage!")
            status["poison"] += 3
            return status["health"], status["poison"]
        elif attack_roll > 0:
            status["health"] -= damage
            print(f"{damage} damage!")
            status["poison"] += 2
            return status["health"], status["poison"]
        else:
            print("Miss!")
            return status["health"], status["poison"]

    def combat_choice(self, status):
        choice = random.randint(1, 2)
        if choice == 1:
            return self.basic_attack(status)
        elif choice == 2:
            return self.poison(status)



