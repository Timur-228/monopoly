
from random import randint


def dice(times=0):
    dice_1 = randint(1, 6)
    dice_2 = randint(1, 6)
    print(dice_1, dice_2)
    if dice_1 == dice_2:
        if times == 2:
            return False
        else:
            return dice(times + 1)
    else:
        summ = dice_1 + dice_2
        return summ

