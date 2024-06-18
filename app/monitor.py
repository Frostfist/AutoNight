import screen_brightness_control as sbc
from app.enums import Mode
from screen_brightness_control.exceptions import ScreenBrightnessError, NoValidDisplayError


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
    def current_state(self) -> Mode:
        return self._current_mode

    def toggle(self, theme: Mode) -> None:
        match theme:
            case Mode.LIGHT:
                self._light_mode()
            case Mode.DARK:
                self._dark_mode()

    def _get_current_mode(self) -> Mode:
        ...

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
