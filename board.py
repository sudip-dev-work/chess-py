import variables as var
import pieces
import game
import debug
import moves
import animations as anim



def init_board(tkinter, window):
  canvas = tkinter.Canvas(
    window,
    width=(var.board_screen_size*var.window_size_raw[1]),
    height=(var.board_screen_size*var.window_size_raw[1]),
    bg = var.background_color_2,
    highlightthickness = 0,
    relief = "flat",
    cursor = "arrow"
    
    )
  canvas.pack(anchor="center", expand=True)
  
  window.update_idletasks()
  
  #make checkers  
  canvas_size = canvas.winfo_reqheight()
  chips_size = (canvas_size/var.board_size)
  padding = var.chips_padding * chips_size #LATER
  
  print(f"{canvas_size}:{chips_size}")

  for row in range(var.board_size):
    for col in range(var.board_size):
      #CHIPS
      color = var.color_scheme[(col+row+1) % 2]
      x1 = (col * chips_size)
      x2 = (x1 + chips_size)
      y1 = (row * chips_size)
      y2 = (y1 + chips_size)
      #window.update_idletasks()
      canvas.create_rectangle(
        x1, y1, x2, y2,
        fill = color,
        tags=("chip", f"{row+1}_{col+1}")
      )
      #BORDER
      ## ## ## ## ## ##
      
  #SPAWN PIECES
  for row in range(len(game.arena8)):
    for col in range(len(game.arena8[row])):
        piece = game.arena8[row][col]

        if piece is not None:
            x = (col + 0.5) * chips_size
            y = (row + 0.5) * chips_size
            xtag = f"{row+1}_{col+1}"
            spawnpc(piece, tkinter, canvas, chips_size, x, y, xtag)

  
  # Debug
  if var.debug:
    debug.mouse_pos(tkinter, window)

  mouse_over_text = debug.create_mouse_over_label(tkinter, window)
  primary_slot_text = debug.create_primary_slot_label(tkinter, window)

  def on_motion(event):
    debug.mouse_over(event, canvas, mouse_over_text)
    selection_grid(canvas)

    if var.active_chip != var.prev_active_chip:
        # Stop previous hover animation
        if var.prev_active_chip is not None:
            anim.animation(
                1, arg1=var.prev_active_chip,
                arg2=canvas, active=False
            )
        # Start new hover animation
        if var.active_chip is not None and var.active_chip != var.primary_chip:
            anim.animation(
                1, arg1=var.active_chip,
                arg2=canvas, active=True
            )
        var.prev_active_chip = var.active_chip
        
  def on_click(event):
      anim.animation(2, arg1=var.prev_primary_chip, arg2=canvas, active=False) #STOP PRIMARY PIECE ANIMATION
      
      debug.mouse_click_1(event, canvas, primary_slot_text)
      anim.animation(2, arg1=var.primary_chip, arg2=canvas, active=True) #START PRIMARY PIECE ANIMATION
      
      if var.primary_chip in var.prev_legal_slots: #check prev prim chip
        move_piece(var.prev_primary_chip, var.primary_chip, canvas, tkinter)#move_piece(i_slot, t_slot)
      else:
          anim.animation(3, canvas, var.prev_primary_chip, True)
      moves.create_moves_rect(moves.get_legal_moves(var.primary_chip), canvas)
      primary_slot_grid(canvas)
      var.prev_legal_slots = moves.coords_to_str(moves.get_legal_moves(var.primary_chip)) #set prev prim chip
      var.prev_primary_chip = var.primary_chip
      
      
  canvas.bind("<Button-1>", on_click)
  canvas.bind("<Motion>", on_motion)  



def selection_grid(canvas):
    canvas.delete("selection")
    if var.active_chip == "None":
        return
    active_slot_pos = var.active_chip.split("_")

    # Remove previous selection borders
    canvas.delete("selection")

    canvas_size = canvas.winfo_height()
    chips_size = canvas_size / var.board_size

    for row in range(var.board_size):
        for col in range(var.board_size):

            if row + 1 == int(active_slot_pos[0]) and col + 1 == int(active_slot_pos[1]):
                width = chips_size * var.slot_selection_border_width
                x1 = col * chips_size + width
                x2 = x1 + chips_size - 2*width
                y1 = row * chips_size + width
                y2 = y1 + chips_size - 2*width

                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="",
                    outline=var.color_scheme[2],
                    width = 2*width,
                    tags="selection"
                )

    # Keep selection borders above pieces
    canvas.tag_raise("selection")
          


def primary_slot_grid(canvas):
    canvas.delete("primary")
    if var.primary_chip == "None":
        return
    primary_slot_pos = var.primary_chip.split("_")

    # Remove previous selection borders
    canvas.delete("primary")

    canvas_size = canvas.winfo_height()
    chips_size = canvas_size / var.board_size

    for row in range(var.board_size):
        for col in range(var.board_size):

            if row + 1 == int(primary_slot_pos[0]) and col + 1 == int(primary_slot_pos[1]):
                width = chips_size * var.slot_selection_border_width
                x1 = col * chips_size + width
                x2 = x1 + chips_size - 2*width
                y1 = row * chips_size + width
                y2 = y1 + chips_size - 2*width

                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="",
                    outline=var.color_scheme[3],
                    width = 2*width,
                    tags="primary"
                )

    # Keep selection borders above pieces
    canvas.tag_raise("primary")
    
    
    
# Resize Sprite
def resize_sprite(sprite, target_size):
    original_size = sprite.width()

    from fractions import Fraction
    scale = Fraction(int(target_size), original_size)

    sprite = sprite.zoom(scale.numerator, scale.numerator)
    sprite = sprite.subsample(scale.denominator, scale.denominator)

    return sprite
  
  

#Spawn Pieces Function
def spawnpc(sym, tkinter, canvas, size, x, y, slot):
    sprite = tkinter.PhotoImage(file=pieces.getpc(sym))
    sprite = resize_sprite(sprite, size*var.pieces_size)

    canvas.create_image(
        x, y,
        image=sprite,
        anchor="center",
        tags=("piece", slot, sym)
    )

    if not hasattr(canvas, "sprites"):
        canvas.sprites = []

    canvas.sprites.append(sprite)
    
    
def move_piece(i_slot, t_slot, canvas, tkinter):
    #print("MOVE_PIECE board.py runnin...")
    subject = canvas.find_withtag(f"piece&&{i_slot}")
    if not subject:
        return
    tags = canvas.gettags(subject[0])
    sym = next(t for t in tags if t not in ("piece", i_slot, "current"))

    iy, ix = map(int, i_slot.split("_"))
    ty, tx = map(int, t_slot.split("_"))

    # 1. detect en passant BEFORE changing anything:
    #    a pawn moves sideways onto an EMPTY square
    is_en_passant = (sym[1:] == "P" and ix != tx and game.arena8[ty-1][tx-1] is None)

    # 2. canvas: remove the moving piece, the normal capture, and the en passant victim
    canvas.delete(subject[0])
    canvas.delete(f"piece&&{t_slot}")
    if is_en_passant:
        canvas.delete(f"piece&&{iy}_{tx}")     # the pawn BESIDE you

    # 3. canvas: draw the moved piece
    chips_size = canvas.winfo_reqheight() / var.board_size
    x = (tx - 0.5) * chips_size
    y = (ty - 0.5) * chips_size
    spawnpc(sym, tkinter, canvas, chips_size, x, y, t_slot)

    # 4. data board
    if is_en_passant:
        game.arena8[iy-1][tx-1] = None         # same row as you, target column
    game.arena8[ty-1][tx-1] = sym
    game.arena8[iy-1][ix-1] = None
    var.last_move = ((iy, ix), (ty, tx), sym)
    
    var.primary_chip = "None"
    var.prev_legal_slots = []
    #print(f"MOVE PIECE INFO :: islot-{i_slot} :: tslot-{t_slot} :: {row}x{col} :: {x}x{y}")