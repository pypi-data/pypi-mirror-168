# import predictions

## Examples

Crash
```py
import predictions

o = predictions.crash
varName = o.crashpredictor()
#  varName returns a dict {{'crashchance': str(chance), 'crashprediction': str(prediction)}
chance = varName[crashchance]
prediction = varName[crashprediction]
print(chance, prediction)
```
Mines
```py
import predictions

o = predictions.mines
output = o.minespredictor(tileo, bombs) # tileo = How many tiles the user wants to open  # bombs = how many bombs on the field
print(output)
```

Towers
```py
import predictions

o = predictions.towers
output = o.towerspredictor()
print(output)
```

Roulette
```py
import predictions

o = predictions.roulette
output = o.roulettepredictor()
print(output)
```

