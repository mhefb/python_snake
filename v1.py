from rendering.ANSIRenderer import ANSIRenderer
import time
import msvcrt
from pynput  import keyboard

rdr: ANSIRenderer = ANSIRenderer()
size_x = 100
size_y = 25
# X, Y size
window_size = (5, 5)
start_pos = (5, 5)
pos_x = lambda c: c*10+start_pos[0]
pos_y = lambda c: c*5+start_pos[1]

spieler_pos = [0,0]

def init():
    for i in range(window_size[0]):
        for j in range(window_size[1]):
            rdr.fill(pos_x(i), pos_y(j), 10, 5, (255,255,255))
    rdr.push_leds()

def spieler_zeichnen(self, delete: bool):
    if not delete:
        rdr.fill(pos_x(spieler_pos[0]), pos_y(spieler_pos[1]), 10, 5, (255,255,255))
    else:
        rdr.fill(pos_x(spieler_pos[0]), pos_y(spieler_pos[1]), 10, 5, (0,255,0))
    rdr.push_leds()

def move(self, k: str):
    if k == 'up':
        spieler_zeichnen(False,False)
        spieler_pos[1] -= 1
        spieler_zeichnen(True,True)
    elif k == 'down':
        spieler_zeichnen(False,False)
        spieler_pos[1] += 1
        spieler_zeichnen(True,True)
    elif k == 'left':
        spieler_zeichnen(False,False)
        spieler_pos[0] -= 1
        spieler_zeichnen(True,True)
    elif k == 'right':
        spieler_zeichnen(False,False)
        spieler_pos[0] += 1
        spieler_zeichnen(True,True)

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'esc':
        return False
    elif k in ('up','down','left','right'):
        move(True,k)

init()
spieler_zeichnen(True,True)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys
