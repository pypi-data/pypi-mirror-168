import random


# Mines predictor code
def minespredictor(tileo, bombs):
    tiles = list(range(1,26))
    totalsquaresleft = 25
    formel = ((totalsquaresleft - bombs) / (totalsquaresleft))
    totalsquareslefts = 24
    formel2 = ((totalsquareslefts - bombs) / (totalsquareslefts))
    for i in range(tileo):
     formel2 *= formel
     totalsquaresleft -= 1
     totalsquareslefts -= 1
     while True:
            tile_to_unlock = random.choice(tiles)
            if tile_to_unlock != "unlocked!":
                tiles[tile_to_unlock] = "unlocked!"
                break
    counter = 0
    output = ""
    for tile in tiles:
        if counter == 5:
            output += "\n"
            counter = 0
        if tile == "unlocked!":
            output += " <:Robbux:1023240704404762675>"
        else:
            output += " <:cadaboom:1023240865382141972> "
        counter += 1
    return output