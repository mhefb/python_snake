from rendering.ANSIRenderer import ANSIRenderer
import time
import msvcrt
from pynput import keyboard
from random import random

global rdr
rdr: ANSIRenderer = ANSIRenderer()
size_x = 100
size_y = 25

pressed_char = ' '

class snake_game():
    """docstring for snake_game."""

    def __init__(self):
        super(snake_game, self).__init__()
        #x, y
        self.window_size = (18, 24)
        self.pixel = (2, 1)
        self.start_pos = (5, 5)
        self.pos_x = lambda c : int(c*self.pixel[0]+self.start_pos[0])
        self.pos_y = lambda c : int(c*self.pixel[1]+self.start_pos[1])
        self.field_color = (255,255,255)
        self.berry_pos = [0,0]
        self.berry_color = (255,0,255)
        self.player_lenght = 2
        #self.player_lenght = self.window_size[0]*self.window_size[1]
        self.player_head_pos = [int(self.window_size[0]/2),int(self.window_size[1]/2)]
        self.player_body_pos = [(self.player_head_pos[0],self.player_head_pos[1])]
        self.player_color = (255,255,0)
        global rdr

        # paints the window
        for i in range(self.window_size[0]):
            for j in range(self.window_size[1]):
                rdr.fill(self.pos_x(i), self.pos_y(j), self.pixel[0], self.pixel[1], self.field_color)
        # first sets the berry
        self.find_new_berry()
        # fist draws the player
        self.draw_player()
        self.update_screen()

    def update_screen(self):
        global rdr
        rdr.push_leds()

    def draw_player(self):
        global rdr
        rdr.fill(self.pos_x(self.player_head_pos[0]), self.pos_y(self.player_head_pos[1]), self.pixel[0], self.pixel[1], self.player_color)
        self.player_body_pos.append(self.player_head_pos.copy())

    def erase_player(self):
        global rdr
        player_tail_pos = self.player_body_pos[0]
        lenght_diference = self.player_lenght - len(self.player_body_pos)
        if lenght_diference <= 0:
            rdr.fill(self.pos_x(player_tail_pos[0]), self.pos_y(player_tail_pos[1]), self.pixel[0], self.pixel[1], self.field_color)
            self.player_body_pos.pop(0)
        elif lenght_diference > 0:
            pass

    def find_new_berry(self):
        global rdr
        counter = 0
        possible_positions = [[]]
        for x in range(self.window_size[0]):
            for y in range(self.window_size[1]):
                if not [x,y] in self.player_body_pos:
                    possible_positions.append((x,y))
        possible_positions.pop(0)
        if len(possible_positions) == 0:
            # player is in every pixel
            print("YOU WON")
            time.sleep(2)
            self.__init__()
        else:
            picked_position = int(random()*len(possible_positions))
            self.berry_pos = [possible_positions[picked_position][0],possible_positions[picked_position][1]]
            rdr.fill(self.pos_x(self.berry_pos[0]), self.pos_y(self.berry_pos[1]), self.pixel[0], self.pixel[1], self.berry_color)

    def player_eats_berry(self):
        self.player_lenght += 1

    def berry_mechanics(self):
        if self.berry_pos == self.player_head_pos:
            self.player_eats_berry()
            self.find_new_berry()

    def game_over(self):
        global rdr
        #round_up = lambda n, div : int(n/div) + (n%div>0)
        smaller_window_side = self.window_size[0] if self.window_size[0] <= self.window_size[1] else self.window_size[1]
        ray_y = lambda h : self.pos_y(h*self.window_size[1]/smaller_window_side) #* self.pixel[1] + self.start_pos[1]
        for i in range(smaller_window_side):
            rdr.fill(self.pos_x(i), ray_y(i), self.pixel[0], self.pixel[1], (255, 0, 0))
            rdr.fill(self.pos_x(self.window_size[0]-1-i), ray_y(i), self.pixel[0], self.pixel[1], (255, 0, 0))
        self.update_screen()
        time.sleep(200000)
        self.__init__()

    def collision_detection_self(self):
        if self.player_head_pos in self.player_body_pos:
            return True
        else:
            return False

    def move(self, direction: str):
        if direction == 'up':
            if self.player_head_pos[1] > 0:
                self.erase_player()
                self.player_head_pos[1] -= 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else: # must be outside the borders
                self.game_over()
        elif direction == 'down':
            if self.player_head_pos[1] + 1 < self.window_size[1]:
                self.erase_player()
                self.player_head_pos[1] += 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else: # must be outside the borders
                self.game_over()
        elif direction == 'left':
            if self.player_head_pos[0] > 0:
                self.erase_player()
                self.player_head_pos[0] -= 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else: # must be outside the borders
                self.game_over()
        elif direction == 'right':
            if self.player_head_pos[0] + 1 < self.window_size[0]:
                self.erase_player()
                self.player_head_pos[0] += 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else: # must be outside the borders
                self.game_over()
        self.berry_mechanics()
        self.update_screen()

def on_press(key):
    global pressed_char
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'esc':
        return False
    if k == pressed_char:
        pass
    else:
        pressed_char = k
    if pressed_char in ('up','down','left','right'):
        game.move(pressed_char)

game = snake_game()

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
#listener.join()

old_presser_char = ' '
while True:
    if pressed_char in ('up','down','left','right'):
        game.move(pressed_char)
        time.sleep(.5)
    elif pressed_char == 'esc':
        continue
