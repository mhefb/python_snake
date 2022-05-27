from rendering.RendererBase import RendererBase
import sys


class ANSIRenderer(RendererBase):
    def fill(self, start_x: int, start_y: int, width: int, height: int, color: (int, int, int)):
        for x in range(width):
            for y in range(height):
                self.set_led(x + start_x, y + start_y, color)
        pass

    def set_led(self, x: int, y: int, color: (int, int, int)):
        # Moves to the position and write the color
        sys.stdout.write(
            "\x1b[" + str(y) + ";" + str(x) + "H\x1b[48;2;" + str(color[0]) + ";" + str(color[1]) + ";" + str(
                color[2]) + "m ")
        pass

    def push_leds(self):
        sys.stdout.flush()
        pass
