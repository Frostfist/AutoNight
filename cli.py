import sys
from app.core.rgb import RgbClient
from app.core.devices import Monitor


def main():
    rgb_client = RgbClient()
    monitor = Monitor()

    if len(sys.argv) < 2:
        print("Our commands: \n\t -n - Dark mode\n\t -l - Light mode")
        sys.exit(1)

    match sys.argv[1]:
        case "-d":
            print("Dark mode")
            monitor.dark_mode()
            rgb_client.clear_devices_lighting()

        case "-l":
            print("Light mode")
            monitor.light_mode()
            rgb_client.reset_lights()

        case "-c":
            print(monitor.current_mode)

        case "-t":
            monitor.toggle()


if __name__ == '__main__':
    main()
