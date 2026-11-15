#Debug
debug = True
labelclr = "#ff0000"

#Window Settings
window_title = "Chess [from scratch]"
window_size_raw = (1100, 800)
window_size = f"{window_size_raw[0]}x{window_size_raw[1]}"
window_minsize = (900, 650)
background_color_1 = "#555555"
background_color_2 = "#000000"

#Board Settings
board_screen_size = 90/100
color_scheme = ("#115511", "#bbffbb", "#44bb44", "#112211")
color_scheme_2 = ("#bb4444", "#ffbbbb") #for tagging moves
board_size = 8
chips_padding = 5/100
chips_outline = "#777777"

#Pieces Settigns
color_type = "duo"
pieces_img_size = 16
pieces_size = 0.8
slot_selection_border_width = 0.025

#IN GAME VARS.
delta_time
mouse_pos = (0,0)
active_chip = "1_1"
primary_chip = "1_1"
legal_moves = []
prev_legal_slots = []          # was "1_1"
prev_primary_chip = "None"     # was "1_1"
last_move = None   # ((from_y, from_x), (to_y, to_x), sym) after every move; needed for en passant