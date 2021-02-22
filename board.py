from tkinter import Tk, Canvas, mainloop, PhotoImage, NW
import Dice
import Jail
from time import sleep
from random import randint, choice


def step(line, a):
    '''Возвращает вектор, на который нужно переместить фишку в зависимоси от положения'''
    return [
        (-a, 0),  # влево
        (0, -a),  # вверх
        (a, 0),  # вправо
        (0, a)  # вниз
    ][line]


class Player:

    def __init__(self, color, obj_id=0):
        self.money = 1_500_000
        self.pos_x, self.pos_y = start_point, start_point
        self.color = color
        self.id = obj_id
        self.line = 0
        self.cell = 0
        self.properties = []
        self.price_of_property = 0
        self.sit_on_place = 0
        self.card_of_freedom = 0
        self.bankrot_status = 0

    def check_if_in_property(self):
        print(
            f'======До хода\n{self.color} состояние: {self.money}, цена недвижимости: {self.price_of_property}\nнедвижимость: {self.properties}')
        for prop in Property_list:
            if self.line == prop.line and self.cell == prop.cell:
                owner = prop.owner
                if owner == None:
                    if self.money >= prop.price:
                        prop.owner = self
                        self.money -= prop.price
                        self.properties.append([prop.name, prop.price])
                        self.price_of_property += prop.price
                        print(f'\n\t{self.color} купил {prop.name}\n')

                else:
                    if owner == self:
                        break
                    if self.money >= prop.price:
                        self.money -= prop.price
                        print(f'\n\t{self.color} заплатил {owner.color} {str(prop.price)} рублей\n')

                    else:
                        price = prop.price
                        if self.price_of_property > price:
                            while price > 0:
                                sold = self.properties.pop()
                                owner.properties.append(sold)
                                price -= sold[1]
                                self.price_of_property -= sold[1]
                                print(f'\n\tу {self.color} конфискуется в пользу {owner.color}\n\n')

                        else:
                            self.properties = []
                            self.money = 0
                            self.price_of_property = 0
                            self.bankrot_status = 1
                            if self.bankrot_status == 0:
                                print(f'\n\t{self.color} банкрот!\n')
        print(
            f'======После хода\n{self.color} состояние: {self.money}, цена недвижимости: {self.price_of_property}\nнедвижимость: {self.properties}')

    def check_if_in_chance(self):
        if self.line == 0 and self.cell == 7 or self.line == 2 and self.cell == 2 or self.line == 3 and self.cell == 6:
            chance = randint(1, 3)
            if chance == 1:
                win = [10000, 20000, 30000, 40000, 50000]
                chance_money = choice(win)
                self.money += chance_money
                print(f'\n\t{self.color} получил {chance_money} рублей\n')
            elif chance == 2:
                chance_move = randint(2, 12)
                self.move(chance_move)
                print(f'\n\t{self.color} передвигается на {chance_move} клеток\n')
            else:
                self.card_of_freedom += 1
                print(self.color + 'получил' + 'освобождение от тюрьмы')


    def check_in_comm_chest(self):
        comm_chest = randint(1, 2)
        if comm_chest == 1:
            lose = [10000, 20000, 30000, 40000, 50000]
            self.money  -= choice(lose)
            print(self.color + 'оставил деньги в общественной казне')
        else:
            Jail.jail(self)


    def check_if_in_free_parking(self):
        if self.cell == 0 and self.line == 2:
            self.sit_on_place += 1

    def check_if_in_tax(self):
        if self.cell == 4 and self.line == 0:
            income_nalog = 200000
            if self.money >= income_nalog:
                self.money -= income_nalog
            else:
                if self.price_of_property >= income_nalog:
                    while income_nalog > 0:
                        sold = self.properties.pop()
                        income_nalog -= sold[1]
                        self.price_of_property -= sold[1]
                        print(f'\n\tу {self.color} конфискуется ')
                else:
                    self.properties = []
                    self.money = 0
                    self.price_of_property = 0
                    self.bankrot_status = 1
                    if self.bankrot_status == 0:
                        print(f'\n\t{self.color} банкрот!\n')
        elif self.cell == 8 and self.line == 3:
            luxury_nalog = 400000
            if self.money >= luxury_nalog:
                self.money -= luxury_nalog
            else:
                if self.price_of_property >= luxury_nalog:
                    while luxury_nalog > 0:
                        sold = self.properties.pop()
                        luxury_nalog -= sold[1]
                        self.price_of_property -= sold[1]
                        print(f'\n\tу {self.color} конфискуется ')
                else:
                    self.properties = []
                    self.money = 0
                    self.price_of_property = 0
                    self.bankrot_status = 1
                    if self.bankrot_status == 0:
                        print(f'\n\t{self.color} банкрот!\n')


    def move(self, n, d=1, delay=0.5):
        '''n -- количество клеток, на которое нужно переместиться
           d -- направление (1 или -1)'''
        if self.money > 0:
            if self.sit_on_place > 0:
                self.sit_on_place -= 1
                sleep(delay)
            else:
                while n > 0:
                    a = 50

                    if not self.cell or self.cell == 9:
                        a = 65

                    canvas.move(self.id, *step(self.line, d * a))
                    tk.update()

                    n -= 1
                    self.cell += d

                    if self.cell > 9 or self.cell < 0:
                        self.cell = 0
                        self.line = (self.line + d) % 4
                    sleep(delay)


    def check_if_in_jail(self):
        if self.cell == 0 and (self.line == 1 or self.line == 3):
            Jail.jail(self)

    def check_if_in_start(self):
        if self.cell == 0 and self.line == 0:
            self.money += 200000


def check_if_game_running():
    num_of_bancrots = 0
    bancrot_list = []
    for player in player_list:
        if player.money <= 0:
            bancrot_list.append(player)
            num_of_bancrots += 1
    if num_of_bancrots >= 3:
        for player in player_list:
            if player not in bancrot_list:
                print(player.color + 'победил!')
        return False
    else:
        return True


def turn():
    """

    """
    for player in player_list:
        dice = Dice.dice()
        if dice == False:
            Jail.jail(player)
        else:
            player.move(dice, delay=0.5)
            player.check_if_in_property()
            player.check_if_in_chance()
            player.check_if_in_jail()
            player.check_if_in_start()
            player.check_if_in_tax()
            player.check_in_comm_chest()
            player.check_if_in_free_parking()


class Property:

    def __init__(self, name, line, cell, price, owner):
        self.price = price
        self.line = line
        self.cell = cell
        self.owner = owner
        self.name = name


Property_list = []
Property_list.append(Property('Electric_company', 1, 2, 150000, None))
Property_list.append(Property('Water_works', 2, 8, 150000, None))
Property_list.append(Property('rail_road_1', 0, 5, 200000, None))
Property_list.append(Property('rail_road_2', 1, 5, 200000, None))
Property_list.append(Property('rail_road_3', 2, 5, 200000, None))
Property_list.append(Property('rail_road_4', 3, 5, 200000, None))
Property_list.append(Property('mediter_avenue', 0, 1, 60000, None))
Property_list.append(Property('baltic_avenue', 0, 3, 60000, None))
Property_list.append(Property('Quental_avenue', 0, 6, 100000, None))
Property_list.append(Property('Vermont_avenue', 0, 8, 100000, None))
Property_list.append(Property('Connecticut_avenue', 0, 9, 100000, None))
Property_list.append(Property('St_Charles_place', 1, 1, 140000, None))
Property_list.append(Property('States_avenue', 1, 3, 140000, None))
Property_list.append(Property('Virginia_avenue', 1, 4, 140000, None))
Property_list.append(Property('St_Sames_place', 1, 6, 180000, None))
Property_list.append(Property('Tennesi_avenue', 1, 8, 180000, None))
Property_list.append(Property('New_York_avenue', 1, 9, 180000, None))
Property_list.append(Property('Kentucki_avenue', 2, 1, 220000, None))
Property_list.append(Property('Bolivia_avenue', 2, 3, 220000, None))
Property_list.append(Property('Illinoise_avenue', 2, 4, 220000, None))
Property_list.append(Property('Atlantic_avenue', 2, 6, 220000, None))
Property_list.append(Property('Texas_avenue', 2, 7, 220000, None))
Property_list.append(Property('Pacific_avenue', 3, 1, 260000, None))
Property_list.append(Property('North_Carolina_avenue', 3, 2, 260000, None))
Property_list.append(Property('Pensilvania_avenue', 3, 4, 260000, None))
Property_list.append(Property('Park_place', 3, 7, 300000, None))
Property_list.append(Property('Board_place', 3, 9, 400000, None))


if __name__ == '__main__':
    start_point = 560
    size = 600
    game_width, game_height = size, size

    tk = Tk()
    tk.title('Монополия!')
    canvas = Canvas(tk, width=game_width, height=game_height, bd=0, highlightthickness=0)

    bg = PhotoImage(file='bg.png')
    canvas.create_image(0, 0, anchor=NW, image=bg)

    r = 14
    colors = ['green', 'yellow', 'red', 'blue']
    player_list = []
    for i in range(4):
        player_list.append(Player(colors[i], canvas.create_oval(start_point - r + i * 5, start_point - r + i * 5,
                                                                start_point + r + i * 5, start_point + r + i * 5,
                                                                fill=colors[i], width=0)))
    canvas.pack()
    tk.update()
    while check_if_game_running():
        turn()
mainloop()
