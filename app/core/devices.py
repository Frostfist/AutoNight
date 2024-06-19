import screen_brightness_control as sbc
from screen_brightness_control.exceptions import ScreenBrightnessError, NoValidDisplayError

from app.core.enums import Mode
from app.core.theme_mode_decorator import ThemeModeDetector

class Monitor:
    def __init__(self, min_brightness: int = 0, max_brightness: int = 50):
        """
        :param max_brightness: maximum brightness to monitor
        :param min_brightness: minimum brightness to monitor
        """
        self._current_mode: Mode = self._get_current_mode()
        self._max_brightness: int = max_brightness
        self._min_brightness: int = min_brightness

    @property
    def current_mode(self) -> Mode:
        """
        :return: current mode
        """
        return self._current_mode

    def toggle(self) -> None:
        """
        Toggle modes.
        :return: None
        """
        if self._current_mode == Mode.LIGHT:
            self._dark_mode()
        if self._current_mode == Mode.DARK:    
            self._light_mode()
        
    @staticmethod
    def _get_current_mode() -> Mode:
        try:
            detector = ThemeModeDetector()
            return detector.get_theme_mode()
        
        except AttributeError:
            print("Detector is not defined")

    def _dark_mode(self) -> None:
        self._current_mode = Mode.DARK
        self._set_brightness(self._min_brightness)

    def _light_mode(self) -> None:
        self._current_mode = Mode.LIGHT
        self._set_brightness(self._max_brightness)

    @staticmethod
    def _set_brightness(brightness: int) -> bool:
        """
        Sets the brightness of the monitor
        :param brightness: brightness to set
        :return: boolean indicating success or failure
        """
        try:
            sbc.set_brightness(brightness)

            return True

        except (ScreenBrightnessError, NoValidDisplayError):
            # logging

            return False

    def light_mode(self):
        return self._light_mode()

    def dark_mode(self):
        return self._dark_mode()
