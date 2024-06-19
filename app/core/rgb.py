from subprocess import Popen, PIPE, TimeoutExpired
from pathlib import Path
from openrgb import OpenRGBClient
from typing import Callable

from app.config.config import SERVER_HOST, SERVER_PORT, APP_PATH
from app.core.decorators import singleton

@singleton
class RgbServer:
    def __init__(self, path_to_open_rgb: Path = APP_PATH) -> None:
        self._path_to_open_rgb = path_to_open_rgb
        self.open_rgb_process: Popen | None = None

    def start(self) -> None:
        return self._start()

    def _start(self):
        try:
            if self.open_rgb_process is not None:
                self.open_rgb_process = Popen(
                    [self._path_to_open_rgb, "--server", "--server-host", SERVER_HOST, "--server-port", SERVER_PORT],
                    stdout=PIPE, stderr=PIPE)

        except (FileNotFoundError, OSError):
            print(f"OpenRGB file is not found! Check the path - {self._path_to_open_rgb}")

        except TimeoutExpired:
            print(f"OpenRGB server is expired! Check if the server is launched.")

    def stop(self) -> None:
        self.open_rgb_process.kill()
        print("Server stopped.")

    def autoexec(self, func: Callable):
        def wrapper(*args, **kwargs) -> None:
            self.start()
            func(*args, **kwargs)
            self.stop()
            return None

        return wrapper


class RgbClient:
    def connect(self) -> None:
        return self._connect()

    def _connect(self) -> None:
        try:
            self._client: OpenRGBClient = OpenRGBClient(address=SERVER_HOST, port=SERVER_PORT)
            self._client.connect()
        except TimeoutError:
            raise TimeoutError(
                "Failed to connect to server. Please check your internet connection. Server can be also turned off.")

    def reset_lights(self) -> None:
        ...

    def clear_devices_lighting(self) -> None:
        try:
            self._client.clear()
        except AttributeError:
            print("No devices available.")
