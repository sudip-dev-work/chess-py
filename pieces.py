import variables as var
import game

#Get sprite path
def getpc(piece):
  #piece = wK
  color = game.sym2color[piece[0]]
  img = game.sym2img[piece[1:]]
  path = f"assets/pieces/{var.color_type}/{color}_{img}.png"
  return path

def coor2pc(coor):
  vec2 = coor.split("_")
  row = int(vec2[0]) - 1
  col = int(vec2[1]) - 1
  piece_symbol = game.arena8[row][col]
  return piece_symbol