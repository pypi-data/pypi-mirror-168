import random




#  Tower predictor
def towerspredictor():
  an = []
  an.clear()
  for i in range(8):
    seq = ["<:Xbozo:1023240762646859896>", "<:Xbozo:1023240762646859896>", "<:Xbozo:1023240762646859896>"]
    a = random.randrange(0, len(seq))
    seq[a] = "<:GOOdx:1023241588102680596>" 
    an.append(" ".join(seq))
  return "\n".join(an)

