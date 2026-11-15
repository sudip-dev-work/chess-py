import game
import variables as var

#spos
#dir(X,+,custom[exp.])
#n(if dir == X or +)
#coll = bool
def add_vec2(a, b) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])
def coor2vec(coor):
  vecstr = coor.split("_")
  vecint = list(map(int, vecstr))
  return vecint #(y,x)
def filter_oob(coor):
    y, x = coor
    return 1 <= y <= var.board_size and 1 <= x <= var.board_size
def coords_to_str(coords: list[tuple[int, int] | None]) -> list[str | None]:
    result = []
    for coord in coords:
        if coord is None:
            result.append(None)
        else:
            y, x = coord
            result.append(f"{y}_{x}")
    return result
def coor2sym(vec2):
    if isinstance(vec2, str):
        y, x = map(int, vec2.split("_"))
    else:
        y, x = vec2
    if not filter_oob((y, x)):      # stops negative indexes from wrapping
        return None
    return game.arena8[y-1][x-1]

def is_en_passant(spos, diag, me):
    last = var.last_move
    if last is None:
        return False
    (fy, fx), (ty, tx), lsym = last
    beside = (spos[0], diag[1])     # square where the enemy pawn must be standing
    return (lsym[1:] == "P" and lsym[0] != me
            and abs(fy - ty) == 2 and (ty, tx) == beside)

def get_legal_moves(scoor):
    blank = []
    if scoor == "None":             # clicked outside the board
        return blank
    sym = coor2sym(scoor)
    if sym is None:                 # clicked an empty square
        return blank
    if sym[1:] == "P":
        return P(scoor)
    return blank                       # other pieces: later

def P(scoor):
    sym = coor2sym(scoor)
    spos = coor2vec(scoor)          # [y, x]
    me = sym[0]
    if me == "w":
        dy, start_row = -1, var.board_size - 1
    else:
        dy, start_row = +1, 2

    legal = []

    # front step, then double step (double only if single is also free)
    front = add_vec2(spos, (dy, 0))
    if filter_oob(front) and coor2sym(front) is None:
        legal.append(front)
        double = add_vec2(spos, (2*dy, 0))
        if spos[0] == start_row and filter_oob(double) and coor2sym(double) is None:
            legal.append(double)

    # diagonals: capture an enemy, or en passant onto an empty square
    for dx in (-1, 1):
        diag = add_vec2(spos, (dy, dx))
        if not filter_oob(diag):
            continue
        target = coor2sym(diag)
        if target is not None and target[0] != me:
            legal.append(diag)
        elif target is None and is_en_passant(spos, diag, me):
            legal.append(diag)
    
    return legal
  
  
  

def create_moves_rect(legal_moves_coords, canvas):
  #UPDATE VAR.LEGAL_MOVES
  var.legal_moves = get_legal_moves(var.primary_chip)
  print(f"Legal Moves : {var.legal_moves}")
  canvas.delete("moves")
  canvas_size = canvas.winfo_reqheight()
  chips_size = (canvas_size/var.board_size)
  indexes = coords_to_str(legal_moves_coords)  
  for row in range(var.board_size):
    for col in range(var.board_size):
      index = f"{row+1}_{col+1}"
      if index in indexes:
        #CHIPS
        color = var.color_scheme_2[(col+row+1) % 2]
        x1 = (col * chips_size)
        x2 = (x1 + chips_size)
        y1 = (row * chips_size)
        y2 = (y1 + chips_size)
        canvas.create_rectangle(
          x1, y1, x2, y2,
          fill = color,
          tags=("moves")
        )
  canvas.tag_raise("piece")
  canvas.tag_raise("selection")
  canvas.tag_raise("primary")
  
  #update and run proxy_markup in game.py
  game.proxy_markup(var.legal_moves)