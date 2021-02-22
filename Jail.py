def find_jail(cell, line):
    n = 10 * (line - 1) + cell
    d = (n > 0) * 2 - 1
    return n, d


def jail(player):
    if player.card_of_freedom > 0:
        player.card_of_freedom -= 1
    else:
        player.move(*find_jail(player.cell, player.line), delay=0.5)
        pay = 50000
        if player.money >= pay:
            player.money -= pay
        else:
            if player.price_of_property >= pay:
                while pay > 0:
                    sold = player.properties.pop()
                    pay -= sold[1]
                    player.price_of_property -= sold[1]
                    print(f'\n\tу {player.color} конфискуется ')
            else:
                player.sit_on_place += 3
