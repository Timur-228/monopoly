from tkinter import Tk, Canvas, mainloop, PhotoImage, NW
import Dice
import Jail
from time import sleep


def step(line, a):
    '''Возвращает вектор, на который нужно переместить фишку в зависимоси от положения'''
    return [
        (-a, 0), # влево
        (0, -a), # вверх
        (a, 0), # вправо
        (0, a) # вниз
    ][line]

class Player:
    
    def __init__(self, color, obj_id=0):
        self.money = 1_500_000
        self.pos_x, self.pos_y = start_point, start_point
        self.color = color
        self.id = obj_id
        self.line = 0
        self.cell = 0

    def player_move(self, n):
        while n > 0:
            a = 50

            if not self.cell or self.cell == 9:
                a = 65

            canvas.move(self.id, *step(self.line, a))
            tk.update()

            print(n, self.line)
            n -= 1
            self.cell += 1

            if self.cell > 9:
                self.cell = 0
                self.line = (self.line + 1) % 4
            sleep(1)


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
        player_list.append(Player(colors[i], canvas.create_oval(start_point - r + i*5, start_point - r + i*5,
                                                            start_point + r + i*5, start_point + r + i*5,
                                                            fill=colors[i], width=0)))
    canvas.pack()
    tk.update()
    player_list[0].player_move(100)
    mainloop()
