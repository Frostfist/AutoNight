from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

# Connect to OpenRGB SDK
client = OpenRGBClient()



try:
    client.clear()
except Exception as e:
    print(e)