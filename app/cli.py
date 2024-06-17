import sys
from monitor import Monitor
from rgb import RgbClient, RgbServer

rgb_server = RgbServer()
rgb_server.start()

def main():
    rgb_client = RgbClient()
    monitor = Monitor()

    if len(sys.argv) < 2:
        print("Usage: %s <solution file>" % sys.argv[0])
        sys.exit(1)

    match sys.argv[1]:
        case "-n":
            print("Night mode")
            monitor.night_mode()
            rgb_client.clear_devices_lighting()

        case "-l":
            print("Light mode")
            monitor.light_mode()
            rgb_client.reset_lights()


if __name__ == '__main__':
    main()
