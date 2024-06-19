from enum import StrEnum


class System(StrEnum):
    WINDOWS = 'windows'
    LINUX = 'linux'
    MACOS = 'darwin'
    UNSUPPORTED = 'unsupported'


class Mode(StrEnum):
    UNKNOWN = "unknown"
    DARK = "dark"
    LIGHT = "light"
