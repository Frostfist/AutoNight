import colorama
import screen_brightness_control as sbc

class Monitor:
    def __init__(self, max_brightness: int = 50, min_brightness: int = 0):
        """

        :rtype: object
        """
        self._max_brightness: int = max_brightness
        self._min_brightness: int = min_brightness
    
    def night_mode(self):
        sbc.set_brightness(self._min_brightness)
    

    def light_mode(self):
        sbc.set_brightness(self._max_brightness)
