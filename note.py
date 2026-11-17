
import pandas as pd
import variables as var
import game


# Piece notation
PIECE_NOTATION = {
    "K": "K",
    "Q": "Q",
    "R": "R",
    "B": "B",
    "Kn": "N",
    "P": "P"
}


# Initialize records
records = pd.DataFrame(columns=["White", "Black"])
records.index.name = "Move"



def add(i_slot, t_slot):

    print("\n--- NOTATION DEBUG ---")
    print("I_SLOT:", i_slot)
    print("T_SLOT:", t_slot)
    print("TURN:", var.turn)
    print("MOVE INDEX:", var.move_index)

    if not isinstance(i_slot, str) or not isinstance(t_slot, str):
        print("INVALID SLOT")
        return

    row, col = map(int, i_slot.split("_"))

    piece = game.arena8_proxy[row][col]

    print("PROXY PIECE:", repr(piece))

    if not isinstance(piece, str):
        print("INVALID PIECE")
        return

    sym = {
        "K": "K",
        "Q": "Q",
        "R": "R",
        "B": "B",
        "Kn": "N",
        "P": "P"
    }.get(piece[1:])

    print("NOTATION SYMBOL:", sym)

    if sym is None:
        print("UNKNOWN PIECE")
        return

    clr = "White" if var.turn == 0 else "Black"

    records.at[var.move_index, clr] = f"{sym}: {i_slot}-{t_slot}"

    print("RECORDED:", records.at[var.move_index, clr])

    if var.turn == 0:
        var.turn = 1
    else:
        var.turn = 0
        var.move_index += 1

    printrec()
    print("----------------------")



def printrec():
    print(
        records.to_string(
            na_rep="—",
            justify="center",
            col_space=12,
            index=True,
            header=True
        )
    )


# Initial values
var.turn = 0
var.move_index = 1
