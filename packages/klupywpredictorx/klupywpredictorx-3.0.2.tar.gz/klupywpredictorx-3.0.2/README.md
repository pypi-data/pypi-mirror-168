# bloxflippackage

## Examples

Crash
```py
import klupywpredictorx

o = klupywpredictorx.crash
varName = o.crashpredictor()
#  varName returns a dict {{'crashchance': str(chance), 'crashprediction': str(prediction)}
chance = varName[crashchance]
prediction = varName[crashprediction]
print(chance, prediction)
```
Mines
```py
import klupywpredictorx

o = klupywpredictorx.mines
output = o.minespredictor(tileo, bombs) # tileo = How many tiles the user wants to open  # bombs = how many bombs on the field
print(output)
```

Towers
```py
import klupywpredictorx

o = klupywpredictorx.towers
output = o.towerspredictor()
print(output)
```
