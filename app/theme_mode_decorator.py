import platform
import subprocess
import winreg
from app.enums import Mode
from importlib.resources import Resource
from typing import Optional, Dict


class ThemeDetector(Resource):
    def get_theme_mode(self) -> str:
        raise NotImplementedError("Must be implemented by subclasses")


class WindowsThemeDetector(ThemeDetector):
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"

    def get_registry_value(self, name: str) -> Optional[int]:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REGISTRY_PATH) as key:
                value, _ = winreg.QueryValueEx(key, name)
                return value
        except (FileNotFoundError, OSError):
            return None

    def get_theme_mode(self) -> Dict[str, Mode]:
        apps_use_light_theme = self.get_registry_value("AppsUseLightTheme")
        system_use_light_theme = self.get_registry_value("SystemUsesLightTheme")

        apps_mode = Mode.LIGHT if apps_use_light_theme == 1 else Mode.DARK if apps_use_light_theme == 0 else Mode.UNKNOWN
        system_mode = Mode.LIGHT if system_use_light_theme == 1 else Mode.DARK if system_use_light_theme == 0 else Mode.UNKNOWN

        return {
            "apps": apps_mode,
            "system": system_mode
        }


class MacOSThemeDetector(ThemeDetector):
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


class ThemeModeDetector:
    def __init__(self):
        self.detector = self.create_detector()

    @staticmethod
    def create_detector() -> Optional[ThemeDetector]:
        os_name = platform.system()
        if os_name == "Windows":
            return WindowsThemeDetector()
        elif os_name == "Darwin":
            return MacOSThemeDetector()
        else:
            return None

    def get_theme_mode(self) -> str:
        if not self.detector:
            return "Unsupported OS"

        theme_modes = self.detector.get_theme_mode()

        if isinstance(theme_modes, dict):
            return f"Apps theme mode: {theme_modes['apps']}, System theme mode: {theme_modes['system']}"
        else:
            return f"System theme mode: {theme_modes}"


if __name__ == "__main__":
    detector = ThemeModeDetector()
    theme_mode = detector.get_theme_mode()
    print(theme_mode)
