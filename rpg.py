import random
import enemies
file = open("stats.txt", "r+")

player_info = {
    "stats": {
        "str": 0,
        "dex": 0,
        "con": 0,
        "wis": 0,
        "int": 0,
        "cha": 0,
    },
    "stat_ability": {
        "str_ability": 0,
        "dex_ability": 0,
        "con_ability": 0,
        "wis_ability": 0,
        "int_ability": 0,
        "cha_ability": 0,
    },
    "status": {
        "health": 0,
        "max_health": 0,
        "ac": 0,
        "poison": 0,
    }
}


def ability_modifier_maker():  # takes the numbers from stats and transforms them into ability modifiers.
    keys = list(player_info["stat_ability"].keys())
    values = list(player_info["stats"].values())
    for v in range(len(values)):
        values[v] = (values[v] - 10) // 2
    for r in range(len(player_info["stat_ability"])):
        player_info["stat_ability"][keys[r]] = values[r]


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


def stat_saver(dictionary):  # will save the stats to stat_sheet.txt.
    dict_list = list(dictionary)
    for j in range(len(dictionary)):
        dict_name = dict_list[j]
        save = open(f'{dict_name}.txt', "w")
        nl = "\n"
        stat_items = list(dictionary[dict_name].values())
        for number in range(len(dictionary[dict_name])):
            value = stat_items[number]
            if number == len(dictionary[dict_name]) - 1:
                nl = ""
            save.write(f'{value}{nl}')
        save.close()


def stat_roll():   # Rolls all the dice needed for one stat.
    dice1, dice2, dice3, dice4 = random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)
    num = [dice1, dice2, dice3, dice4]
    num.sort()
    num.pop(0)
    total = 0
    for a in num:
        total += a
    return total


def stat_maker():
    st, d, c, w, i, ch = stat_roll(), stat_roll(), stat_roll(), stat_roll(), stat_roll(), stat_roll()
    raw_nums = [st, d, c, w, i, ch]
    empty = []
    print(f'{st}, {d}, {c}, {w}, {i}, and {ch} are your stats')

    for s in player_info["stats"]:
        a = "a"
        while a not in raw_nums:
            x_temp = input(f"What do you want to assign to {s}?\n")
            try:
                x_temp = int(x_temp)
                if x_temp not in raw_nums:
                    print("That's not an option!")
                else:
                    a = x_temp
                    player_info["stats"][s] = a
            except ValueError:
                print("That's not an option!")
        raw_nums.remove(player_info["stats"][s])
        if raw_nums != empty:
            print(raw_nums)
    ability_modifier_maker()
    player_info["status"]["health"] = random.randint(1, 8) + player_info["stat_ability"]["con_ability"]
    player_info["status"]["max_health"] = player_info["status"]["health"]
    player_info["status"]["ac"] = 10 + player_info["stat_ability"]["dex_ability"]


def loading_system():
    filed = open("stats.txt", "r+")
    file_tester = filed.read()

    if file_tester:
        dict_list = list(player_info)
        for i in range(len(player_info)):
            dict_name = dict_list[i]
            filer = open(f'{dict_name}.txt')
            dict_file = filer.read()
            dict_key = list(player_info[dict_name])
            dict_file = dict_file.split("\n")
            for j in range(len(player_info[dict_name])):
                dict_final = dict_key[j]
                player_info[dict_name][dict_final] = int(dict_file.pop(0))
            filer.close()

        answer_options = ["yes", "no"]
        file_answer = 0
        print(f'Do you want to load your old save with stats:\n{player_info["stats"]} \nYes/No')
        while file_answer not in answer_options:
            x = input()
            if str.lower(x) in answer_options:
                file_answer = str.lower(x)
            else:
                print("please enter \'yes\' or \'no\'")

        if file_answer != "yes":
            stat_maker()
    else:
        stat_maker()


def basic_attack(mod, mod2, hp):  # calculates the damage and gives info to the player.
    d20roll = d20()
    attack_roll = d20roll + mod - mod2
    damage = (random.randint(1, 6) + mod)
    if d20roll == 1:
        return hp
    elif d20roll == 20:
        hp -= damage
        print(f"{damage} damage!")
        return hp
    elif attack_roll > 0:
        hp -= damage
        print(f"{damage} damage!")
        return hp
    else:
        print("Miss!")
        return hp


def combat_choice():  # not sure if needed, but helpful because it can be built upon for more complex combat.
    choices = ["flee", "attack"]
    choice1, choice2 = choices
    choice = 0
    while choice not in choices:
        choice = input(f'What do you want to do?\n{choice1}\n{choice2}\n')
        choice = choice.lower()
        if choice not in choices:
            print("Please choose a valid option.")
    return choice


def flee(mod1, mod2):  # like basic attack, but with fleeing.
    d20roll = d20()
    escape_roll = (d20roll + mod1) - mod2
    if d20roll == 1:
        return False
    elif d20roll == 20:
        return True
    elif escape_roll > 0:
        return True


def basic_combat(player, status, enemy):  # if the right information is in here, it should allow the player to fight.
    vowels = ["a", "e", "i", "o", "u"]
    if enemy.name[0:1] in vowels:
        grammar = "an"
    else:
        grammar = "a"
    print(f'You have encountered {grammar} {enemy.name}!')

    while enemy.health or player["health"] > 0:
        choice = combat_choice()
        if choice == "attack":
            enemy.health = basic_attack(player["str_ability"], enemy.ac, enemy.health)
            if enemy.health < 1:
                print(f'You defeated the {enemy.name}')
                return
            print(f'The {enemy.name} has {enemy.health} health left.')
        elif choice == "flee":
            escape = flee(player["dex_ability"], enemy.dex)
            if escape:
                print(f'You escaped the {enemy.name}')
                return
            else:
                print("You failed to escape!")

        print(f'The {enemy.name} attacks you!')
        status["health"] = basic_attack(enemy.str, status["ac"], status["health"])
        print(f'You have {status["health"]} health left.')
        if status["poison"]:
            status["health"] = status["health"] - 1
            print("You took one poison damage!")
            status["poison"] -= 1
        if status["health"] < 1:
            print("You have died. Game over!")
            exit()


loading_system()
randMon = enemies.Monster("slime")

basic_combat(player_info["stat_ability"], player_info["status"], randMon)
stat_saver(player_info)
print(player_info["stats"])
print(player_info["stat_ability"])
