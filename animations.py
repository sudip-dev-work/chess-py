import math
import time
import variables as var
from PIL import Image, ImageTk

RUNNING_LOOPS = {}


def animation(i, arg1="", arg2="", active=True):
  if i == 1: pass#active_piece(arg1, arg2, active)
  if i == 2: primary_piece(arg1, arg2, active)
  if i == 3: move_na(arg1, arg2, active)
  else:return "NO ANIMATION OF THIS INDEX (animations.py)"


def active_piece(arg1, arg2, active=True):
    tag = str(arg1)
    canvas = arg2

    # Find piece image
    items = canvas.find_withtag(tag)
    image_id = next(
        (item for item in items if canvas.type(item) == "image"),
        None
    )

    if image_id is None:
        return

    # STOP: return to original position
    if not active:
        if tag in RUNNING_LOOPS:
            data = RUNNING_LOOPS[tag]

            if data["after_id"] is not None:
                try:
                    canvas.after_cancel(data["after_id"])
                except ValueError:
                    pass

            origin_x, origin_y = data["origin"]
            canvas.coords(image_id, origin_x, origin_y)

            RUNNING_LOOPS.pop(tag, None)
        return

    # Already active
    if tag in RUNNING_LOOPS:
        return

    coords = canvas.coords(image_id)
    origin_x, origin_y = coords[:2]

    hover_distance = (canvas.winfo_height() / var.board_size) * 0.03

    duration = 0.2
    start_time = time.perf_counter()

    RUNNING_LOOPS[tag] = {
        "after_id": None,
        "origin": (origin_x, origin_y)
    }

    def hover_once():
        if tag not in RUNNING_LOOPS:
            return

        progress = min(
            (time.perf_counter() - start_time) / duration,
            1.0
        )

        eased = progress * progress * (3 - 2 * progress)

        canvas.coords(
            image_id,
            origin_x,
            origin_y - hover_distance * eased
        )

        if progress < 1.0:
            RUNNING_LOOPS[tag]["after_id"] = canvas.after(16, hover_once)
        else:
            RUNNING_LOOPS[tag]["after_id"] = None

    hover_once()
    
    
def primary_piece(arg1, arg2, active=True):
  tag = arg1  # arg1: piece/coordinates with underscores
  tag2 = "piece"
  canvas = arg2  # arg2: canvas
  combined_tag = f"{tag}&&{tag2}"

  # --- STOP TRIGGER ---
  if not active:
    if tag in RUNNING_LOOPS:
      loop_data = RUNNING_LOOPS.pop(tag)
      canvas.after_cancel(loop_data["after_id"])
      origin_x, origin_y = loop_data["origin"]
      if canvas.find_withtag(combined_tag):
        canvas.coords(combined_tag, origin_x, origin_y)
    return

  if tag in RUNNING_LOOPS:
    return

  # 1. Get exact placement where the image is right now as origin
  coords = canvas.coords(combined_tag)
  if not coords:
    return

  origin_x, origin_y = coords[0], coords[1]
  
  canvas_size = canvas.winfo_height()
  chips_size = canvas_size / var.board_size

  # 2. Calculate max bob distance in pixels from var.chips_size
  bob_distance = chips_size * 0.03
  start_time = time.perf_counter()

  def hover_loop():
    if tag not in RUNNING_LOOPS or not canvas.find_withtag(combined_tag):
      RUNNING_LOOPS.pop(tag, None)
      return

    t = time.perf_counter() - start_time

    # Smooth wave from 0.0 to 1.0 (starts at 0 at t=0)
    wave = (1.0 - math.cos(t * 4.0)) / 2.0

    # Bob upward from origin_y to (origin_y - chips_size / 3)
    # Change '-' to '+' if you want it to bob downward instead
    new_y = origin_y - (bob_distance * wave)

    canvas.coords(combined_tag, origin_x, new_y)
    RUNNING_LOOPS[tag]["after_id"] = canvas.after(16, hover_loop)

  RUNNING_LOOPS[tag] = {"after_id": None, "origin": (origin_x, origin_y)}
  hover_loop()


  
def move_na(arg1, arg2, active=True):
  canvas = arg1
  tag = str(arg2)

  # Find the actual image item
  items = canvas.find_withtag(tag)
  if not items:
    return

  image_id = next(
    (item for item in items
     if canvas.type(item) == "image"),
    None
  )

  if image_id is None:
    return

  # --- STOP TRIGGER ---
  if not active:
    if tag in RUNNING_LOOPS:
      loop_data = RUNNING_LOOPS.pop(tag)

      after_id = loop_data.get("after_id")
      if after_id:
        try:
          canvas.after_cancel(after_id)
        except ValueError:
          pass

      origin_x, origin_y = loop_data["origin"]
      canvas.coords(image_id, origin_x, origin_y)

    return

  if tag in RUNNING_LOOPS:
    return

  coords = canvas.coords(image_id)
  if len(coords) < 2:
    return

  origin_x, origin_y = coords[:2]

  start_time = time.perf_counter()
  duration = 0.5

  chips_size = canvas.winfo_height() / var.board_size
  shake_distance = chips_size * 0.05

  def shake_loop():
    if tag not in RUNNING_LOOPS:
      return

    if not canvas.find_withtag(image_id):
      RUNNING_LOOPS.pop(tag, None)
      return

    t = time.perf_counter() - start_time
    progress = min(t / duration, 1.0)

    if progress >= 1.0:
      canvas.coords(image_id, origin_x, origin_y)
      RUNNING_LOOPS.pop(tag, None)
      return

    intensity = 1.0 - progress

    oscillation = math.sin(progress * math.pi * 10)

    offset_x = shake_distance * intensity * oscillation
    offset_y = shake_distance * 0.25 * intensity * math.sin(
      progress * math.pi * 10 + math.pi / 2
    )

    canvas.coords(
      image_id,
      origin_x + offset_x,
      origin_y + offset_y
    )

    RUNNING_LOOPS[tag]["after_id"] = canvas.after(16, shake_loop)

  RUNNING_LOOPS[tag] = {
    "after_id": None,
    "origin": (origin_x, origin_y)
  }

  shake_loop()
