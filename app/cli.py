import sys
from monitor import Monitor
from rgb import RgbClient, RgbServer




def main():
    rgb_client = RgbClient()
    monitor = Monitor()

    if len(sys.argv) < 2:
        print("Usage: %s <solution file>" % sys.argv[0])
        sys.exit(1)

    match sys.argv[1]:
        case "-n":
            print("Night mode")
            monitor._set_brightness()
            rgb_client.clear_devices_lighting()

        case "-l":
            print("Light mode")
            monitor._set_light_theme()
            rgb_client.reset_lights()


if __name__ == '__main__':
    main()
