import platform
import subprocess
import winreg

from typing import Optional
from app.core.enums import Mode, System
from importlib.resources import Resource


class IThemeDetector(Resource):
    def get_theme_mode(self) -> Optional[Mode]:
        raise NotImplementedError("Must be implemented by subclasses")


class Windows(IThemeDetector):
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"

    def get_registry_value(self, name: str) -> Optional[int]:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REGISTRY_PATH) as key:
                value, _ = winreg.QueryValueEx(key, name)
                return value
        except (FileNotFoundError, OSError):
            return None

    def get_theme_mode(self) -> Mode:
        system_use_light_theme = self.get_registry_value("SystemUsesLightTheme")
        system_mode = Mode.LIGHT if system_use_light_theme == 1 else Mode.DARK if system_use_light_theme == 0 else Mode.UNKNOWN

        return system_mode

class MacOs(IThemeDetector):
    def get_theme_mode(self) -> Mode:
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
                check=True
            )
            return Mode.DARK if "Dark" in result.stdout else Mode.LIGHT
        except subprocess.CalledProcessError:
            return Mode.UNKNOWN


def create_detector() -> IThemeDetector:
    os_name = platform.system()
    match os_name:
        case System.WINDOWS:
            return Windows()
        case System.MACOS:
            return MacOs()
        case _:
            return Windows()


class ThemeModeDetector:
    def __init__(self):
        self.detector: IThemeDetector = create_detector()
        print(self.detector)

    def get_theme_mode(self) -> Mode:
        return self.detector.get_theme_mode()


if __name__ == "__main__":
    detector = ThemeModeDetector()
    theme_mode = detector.get_theme_mode()

    print(theme_mode)
