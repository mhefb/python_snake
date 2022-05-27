class RendererBase:
    # Fills the pixels from start to end with the given color
    def fill(self, start_x: int, start_y: int, width: int, height: int, color: (int, int, int)):
        pass

    def set_led(self, x: int, y: int, color: (int, int, int)):
        pass

    def push_leds(self):
        pass
