# bloxflippackage

## Examples

Crash
```py
import bloxflippredictor

o = bloxflippredictor.crash
varName = o.crashpredictor()
#  varName returns a dict {{'crashchance': str(chance), 'crashprediction': str(prediction)}
chance = varName[crashchance]
prediction = varName[crashprediction]
print(chance, prediction)
```
Mines
```py
import bloxflippredictor

o = bloxflippredictor.mines
output = o.minespredictor(tileo, bombs) # tileo = How many tiles the user wants to open  # bombs = how many bombs on the field
print(output)
```

Towers
```py
import bloxflippredictor

o = bloxflippredictor.towers
output = o.towerspredictor()
print(output)
```

Roulette
```py
import bloxflippredictor

o = bloxflippredictor.roulette
output = o.roulettepredictor()
print(output)
```

