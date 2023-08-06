import random




#  Tower predictor
def towerspredictor():
  an = []
  an.clear()
  for i in range(8):
    seq = [":red_circle:", ":red_circle:", ":red_circle:"]
    a = random.randrange(0, len(seq))
    seq[a] = ":green_circle:" 
    an.append(" ".join(seq))
  return "\n".join(an)

