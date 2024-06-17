from subprocess import Popen, PIPE, TimeoutExpired
from pathlib import Path
from openrgb import OpenRGBClient
from config.config import PATH_TO_OPEN_RGB_APP
from decorators import singleton


@singleton
class RgbServer:
    def __init__(self, path_to_open_rgb: Path = PATH_TO_OPEN_RGB_APP, ip: str = "127.0.0.1", port: int = 6742) -> None:
        self._path_to_open_rgb = path_to_open_rgb
        self.open_rgb_process: Popen | None = None
        self.ip = ip
        self.port = port

    def start(self) -> None:
        try:
            if self.open_rgb_process is not None:
                self.open_rgb_process = Popen([self._path_to_open_rgb, "--server", "--ip", self.ip, "--port", self.port], stdout=PIPE, stderr=PIPE)

        except (FileNotFoundError, OSError):
            print(f"OpenRGB file is not found! Check the path - {self._path_to_open_rgb}")

        except TimeoutExpired:
            print(f"OpenRGB server is expired! Check if the server is launched.")

        print("Server started.")

    def stop(self) -> None:
        self.open_rgb_process.kill()
        print("Server stopped.")

    def autoexec(self, func):
        def wrapper(*args, **kwargs) -> None:
            self.start()
            func(*args, **kwargs)
            self.stop()
            return None

        return wrapper


class RgbClient:
    def  __init__(self, ip: str = "127.0.0.1", port: int = 6742):
        try:
            self._client = OpenRGBClient(address=ip, port=port)
        except TimeoutError:
            raise TimeoutError(
                "Failed to connect to server. Please check your internet connection. Server can be also turned off.")

    def reset_lights(self):
        ...

    def clear_devices_lighting(self):
        self._client.clear()
