# bloxflippackage

## Examples

Crash
```py
import klupywpredictorss

o = klupywpredictorss.crash
varName = o.crashpredictor()
#  varName returns a dict {{'crashchance': str(chance), 'crashprediction': str(prediction)}
chance = varName[crashchance]
prediction = varName[crashprediction]
print(chance, prediction)
```
Mines
```py
import klupywpredictorss

o = klupywpredictorss.mines
output = o.minespredictor(tileo, bombs) # tileo = How many tiles the user wants to open  # bombs = how many bombs on the field
print(output)
```

Towers
```py
import klupywpredictorss

o = klupywpredictorss.towers
output = o.towerspredictor()
print(output)
```
