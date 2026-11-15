import tkinter as tk
import variables as var
import board as brd
from pieces import getpc
import debug
import moves

print("[ Running 'main.py' ]")

#Init Window
window = tk.Tk()
window.title(var.window_title)
window.geometry(var.window_size)
window.minsize(*var.window_minsize)
#Configure Window
window.configure(bg=var.background_color_1)

brd.init_board(tk, window)
#moves.moves_canvas(tk, window)

#Loop Window
window.mainloop()