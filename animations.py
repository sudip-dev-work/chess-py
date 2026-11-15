import math
import time


def animation(i, arg1="", arg2=""):
  if i == 1:
    return active_piece(arg1, arg2)
  if i == 2:
    return primary_piece(arg1, arg2)
  else:
    return "NO ANIMATION OF THIS INDEX (animations.py)"


def active_piece(arg1, arg2):
  pass


def primary_piece(arg1, arg2):
  tag = arg1  # arg1 : piece/coordinates with underscores
  tag2 = "piece"
  canvas = arg2  # arg2 : canvas

  # Match items that have BOTH `tag` AND `tag2`
  combined_tag = f"{tag}&&{tag2}"

  # Get the initial (x, y) coordinates of the image matching both tags
  coords = canvas.coords(combined_tag)
  if not coords:
    return  # Exit safely if no item matches both tags

  start_x, base_y = coords, coords
  start_time = time.perf_counter()

  def hover_loop():
    # Stop cleanly if the tagged image is deleted or loses either tag
    if not canvas.find_withtag(combined_tag):
      return

    t = time.perf_counter() - start_time
    # Hover up and down by 6 pixels around base_y
    new_y = base_y + 6 * math.sin(t * 4.0)

    canvas.coords(combined_tag, start_x, new_y)
    canvas.after(16, hover_loop)  # Loop smoothly at ~60 FPS

  hover_loop()
