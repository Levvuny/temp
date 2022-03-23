import random


def old_man():
    answer = input("You find an old man on the road. What do you do?\nApproach/Leave\n")
    answer = answer.lower()
    answers = ["approach", "leave"]
    while answer not in answers:
        print("Please put approach or leave.")
        answer = input().lower()

    print("A")


old_man()
