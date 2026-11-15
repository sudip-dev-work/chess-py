import variables as var
import pieces
import game

labels = {}


def labelv(name):
    label_name, y = name.rsplit("_", 1)
    label = labels[label_name]

    if var.debug:
        label.place(x=10, y=int(y))
    else:
        label.place_forget()


def mouse_pos(tkinter, window):
    labels["mouse_pos_text"] = tkinter.Label(
        window,
        text="Mouse: 0, 0",
        font=("Arial", 12),
        bg=var.labelclr,
        fg="white"
    )

    labelv("mouse_pos_text_10")

    def update_pos(event):
      x = event.x_root - window.winfo_rootx()
      y = event.y_root - window.winfo_rooty()

      labels["mouse_pos_text"].config(
          text=f"Mouse: {x}, {y}"
      )
      var.mouse_pos = (x, y)
    window.bind("<Motion>", update_pos)


def create_mouse_over_label(tkinter, window):
    labels["mouse_over_text"] = tkinter.Label(
        window,
        text="Chip: None",
        font=("Arial", 12),
        bg=var.labelclr,
        fg="white"
    )

    labelv("mouse_over_text_30")

    return labels["mouse_over_text"]

def create_primary_slot_label(tkinter, window):
    labels["primary_slot_text"] = tkinter.Label(
        window,
        text="Chip: None",
        font=("Arial", 12),
        bg=var.labelclr,
        fg="white"
    )
    labelv("primary_slot_text_50")
    return labels["primary_slot_text"]
    
    
def mouse_over(event, canvas, mouse_over_text):
    items = canvas.find_overlapping(
        event.x, event.y,
        event.x, event.y
    )

    chip = next(
        (
            canvas.gettags(item)[1]
            for item in items
            if "chip" in canvas.gettags(item)
        ),
        "None"
    )

    mouse_over_text.config(text=f"Chip: {chip}")
    var.active_chip = chip
    #print(f"Chip: {var.active_chip}")
    
def mouse_click_1(event, canvas, primary_slot_text):
    items = canvas.find_overlapping(
        event.x, event.y,
        event.x, event.y
    )

    chip = next(
        (
            canvas.gettags(item)[1]
            for item in items
            if "chip" in canvas.gettags(item)
        ),
        "None"
    )

    primary_slot_text.config(text=f"Chip: {chip}")
    var.primary_chip = chip
    print(f"Primary Chip: {var.primary_chip} :: {pieces.coor2pc(chip)}[{game.symbol_2_name(pieces.coor2pc(chip))[0]}:::{game.symbol_2_name(pieces.coor2pc(chip))[1]}]")
    