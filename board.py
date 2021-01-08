from tkinter import Tk, Canvas, mainloop, PhotoImage, NW
import Dice
import Jail


class Player:
    def __init__(self, color, obj_id=0):
        self.money = 1_500_000
        self.pos_x, self.pos_y = start_point, start_point
        self.color = color
        self.id = obj_id


def player_move():
    for i in range(len(players_list)):
        if Dice.dice() == False:
            Jail.jail()
        else:
            """хз, как нормально реализовать движение"""
            pass


if __name__ == '__main__':
    start_point = 740
    size = 800
    game_width, game_height = size, size

    tk = Tk()
    tk.title('Монополия!')
    canvas = Canvas(tk, width=game_width, height=game_height, bd=0, highlightthickness=0)

    bg = PhotoImage(file='bg.png')
    canvas.create_image(0, 0, anchor=NW, image=bg)

    r = 14
    colors = ['green', 'yellow', 'red', 'blue']
    players_list = []
    for i in range(4):
        players_list.append(Player(colors[i], canvas.create_oval(start_point - r , start_point - r,
                                                            start_point + r, start_point + r,
                                                            fill=colors[i], width=0)))
    canvas.pack()
    player_move()
    mainloop()