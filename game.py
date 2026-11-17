import variables as var
import moves

def enemy_color(self_color):
  enemy_color = "b" if self_color == "w" else "w"
  return enemy_color
  
def print_board(board, empty="."):
    width = max(len(p) for row in board for p in row if p)
    width = max(width, len(empty), 2)

    header = "    " + " ".join(str(c + 1).center(width) for c in range(len(board[0])))
    line = "   +" + "-" * ((width + 1) * len(board[0]) + 1)

    ###########################print(header)
    ###########################print(line)
    for r, row in enumerate(board):
        cells = " ".join((p if p else empty).center(width) for p in row)
        ###########################print(f"{r + 1:>2} | {cells} |")
    ###########################print(line)

#dictionaries
sym2name = {
  "A":"Amazon",
  "B":"Bishop",
  "E":"Elephant",
  "Em":"Empress",
  "Eh":"Equihopper",
  "Fd":"FD",
  "Fz":"Ferz",
  "G":"Giraffe",
  "K":"King",
  "Kn":"Knight",
  "Kn45":"Knight-45",
  "P":"Pawn",
  "Pq":"Pawn-Queen",
  "Pr":"Princess",
  "Q":"Queen",
  "R":"Rook",
  "S":"Superknight",
  "U":"Unicorn",
  "W":"WFA",
  "Z":"Zebra"
}

sym2img = {
  "A":"amazon",
  "B":"bishop",
  "E":"elephant",
  "Em":"empress",
  "Eh":"equihopper",
  "Fd":"fd",
  "Fz":"ferz",
  "G":"giraffe",
  "K":"king",
  "Kn":"knight",
  "Kn45":"knight45",
  "P":"pawn",
  "Pq":"pawnqueen",
  "Pr":"princess",
  "Q":"queen",
  "R":"rook",
  "S":"superknight",
  "U":"unicorn",
  "W":"wfa",
  "Z":"zebra"
}

sym2color = {
  "b":"Black",
  "w":"White",
  "n":"Neutral"
}

def xproxy_markup(legal_moves_raw):
  if var.primary_chip == "None":
    return
  #legal_moves has no underscores its raw
  #clear board
  arena8_proxy = [row[:] for row in arena8]
  #set primary slot
  primary_slot = (var.primary_chip).split("_")
  primary_slot = list(map(int, primary_slot))
  arena8_proxy[primary_slot[0]-1][primary_slot[1]-1] = f"[{arena8_proxy[primary_slot[0]-1][primary_slot[1]-1]}]"
  #set moves slots
  for move in legal_moves_raw:
    arena8_proxy[move[0]-1][move[1]-1] = "X"
  print_board(arena8_proxy, ".")
def proxy_markup(legal_moves_raw):
  arena8_proxy = [row[:] for row in arena8]       # copy, never the real board

  if var.primary_chip != "None":                  # mark only when something is selected
    r, c = map(int, var.primary_chip.split("_"))
    cell = arena8_proxy[r-1][c-1]
    arena8_proxy[r-1][c-1] = f"[{cell if cell else '.'}]"
    for y, x in legal_moves_raw:
      cell = arena8_proxy[y-1][x-1]
      arena8_proxy[y-1][x-1] = "X" if cell is None else f"x{cell}"

  print_board(arena8_proxy, ".")
  

arena8 = [
    ["bR", "bKn", "bB", "bQ", "bK", "bB", "bKn", "bR"],
    ["bP", "bP" , "bP", "bP", "bP", "bP", "bP" , "bP"],
    [None, None, None, None, None, None, None, None ],
    [None, None, None, None, None, None, None, None ],
    [None, None, None, None, None, None, None, None ],
    [None, None, None, None, None, None, None, None ],
    ["wP", "wP" , "wP", "wP", "wP", "wP", "wP" , "wP"],
    ["wR", "wKn", "wB", "wQ", "wK", "wB", "wKn", "wR"]
]

arena8_proxy = [
    ["bR", "bKn", "bB", "bQ", "bK", "bB", "bKn", "bR"],
    ["bP", "bP" , "bP", "bP", "bP", "bP", "bP" , "bP"],
    [None, None, None, None, None, None, None, None, ],
    [None, None, None, None, None, None, None, None, ],
    [None, None, None, None, None, None, None, None, ],
    [None, None, None, None, None, None, None, None, ],
    ["wP", "wP" , "wP", "wP", "wP", "wP", "wP" , "wP"],
    ["wR", "wKn", "wB", "wQ", "wK", "wB", "wKn", "wR"]
]


arena20 = [
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [],
  [] 
]

def symbol_2_name(sym):
  if sym is None:
    return "None", "Blank"
  color = sym2color[sym[0]]
  name = sym2name[sym[1:]]
  return color, name