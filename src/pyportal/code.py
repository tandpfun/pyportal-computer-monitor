# Import Packages
import board
import displayio
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_button import Button
import adafruit_touchscreen
from adafruit_pyportal import PyPortal
import supervisor
import json
import time

# Define Functions
def set_image(group, filename):
    """Set the image file for a given goup for display.
    This is most useful for Icons or image slideshows.
        :param group: The chosen group
        :param filename: The filename of the chosen image
    """
    print("Set image to ", filename)
    if group:
        group.pop()

    if not filename:
        return  # we're done, no icon desired

    image_file = open(filename, "rb")
    image = displayio.OnDiskBitmap(image_file)
    try:
        image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter())
    except TypeError:
        image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter(),
                                          position=(0, 0))
    group.append(image_sprite)

def showLayer(show_target):
    try:
        time.sleep(0.1)
        splash.append(show_target)
    except ValueError:
        pass

def hideLayer(hide_target):
    try:
        splash.remove(hide_target)
    except ValueError:
        pass

# Setup Display
display = board.DISPLAY
display.rotation = 0

# Setup Touchscreen
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(320, 240))

# Create View Groups
splash = displayio.Group(max_size=25)
normalView = displayio.Group(max_size=15)
detailView = displayio.Group(max_size=15)
detailed = False

# Set text, font, and color
main_font = bitmap_font.load_font("/fonts/HelveticaNeue-24.bdf")
extra_font = bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf")

white = 0xFFFFFF
green = 0x2ecc71
yellow = 0xF1C40F
red = 0xE74C3C
blue = 0x3498DB

# Create the text labels
cpu_label = label.Label(main_font, text='CPU: ...', color=white, max_glyphs=100)
ram_label = label.Label(main_font, text='RAM: ...', color=white, max_glyphs=100)
gpu_label = label.Label(main_font, text='GPU: ...', color=white, max_glyphs=100)
disk_label = label.Label(main_font, text='SSD: ...', color=white, max_glyphs=100)

ram_detail = label.Label(extra_font, text='..G/..G', color=blue, max_glyphs=100)
disk_detail = label.Label(extra_font, text='..G/..G', color=blue, max_glyphs=100)
gpu_temp = label.Label(extra_font, text='.. °C', color=red, max_glyphs=100)

toggle_label = label.Label(extra_font, text='Basic', color=white, max_glyphs=100)

# Set the locations
cpu_label.x = 55
cpu_label.y = 33

ram_label.x = 55
ram_label.y = 90

gpu_label.x = 55
gpu_label.y = 146

disk_label.x = 55
disk_label.y = 203

gpu_temp.x = 210
gpu_temp.y = 146

disk_detail.x = 210
disk_detail.y = 203

ram_detail.x = 210
ram_detail.y = 90

toggle_label.x = 270
toggle_label.y = 10

# Set Background
set_image(normalView, '/images/monitor_background.bmp')

# Show View Groups
normalView.append(cpu_label)
normalView.append(ram_label)
normalView.append(gpu_label)
normalView.append(disk_label)

normalView.append(toggle_label)

detailView.append(gpu_temp)
detailView.append(ram_detail)
detailView.append(disk_detail)

display.show(splash)
showLayer(normalView)

# Function to handle incoming serial data
def handleSerial():
    value = input().strip()
    # Sometimes Windows sends an extra (or missing) newline - ignore them
    if value == "":
        return
    print(f"Received data!")
    jsonData = json.loads(value)
    cpu_label.text = f"CPU: {jsonData['cpu']['percent']}%"
    # For temp:  | {jsonData['cpu']['temp']} °C
    if float(jsonData['cpu']['percent']) > 90:
        cpu_label.color=red
    elif float(jsonData['cpu']['percent']) > 75:
        cpu_label.color=yellow
    else:
        cpu_label.color=green

    ram_label.text = f"RAM: {jsonData['ram']['percent']}%"
    if float(jsonData['ram']['percent']) > 90:
        ram_label.color=red
    elif float(jsonData['ram']['percent']) > 75:
        ram_label.color=yellow
    else:
        ram_label.color=green

    if jsonData['gpu']['percent']:
        gpu_label.text = f"GPU: {jsonData['gpu']['percent']}%"
        if float(jsonData['gpu']['percent']) > 90:
            gpu_label.color=red
        elif float(jsonData['gpu']['percent']) > 75:
            gpu_label.color=yellow
        else:
            gpu_label.color=green
    else:
        gpu_label.text = f"GPU: ...%"
        gpu_label.color=green

    disk_label.text = f"SSD: {jsonData['disk']['percent']}%"
    if float(jsonData['disk']['percent']) > 90:
        disk_label.color=red
    elif float(jsonData['disk']['percent']) > 80:
        disk_label.color=yellow
    else:
        disk_label.color=green

    ram_detail.text = f"{jsonData['ram']['used']}G/{jsonData['ram']['total']}G"
    disk_detail.text = f"{jsonData['disk']['used']}G/{jsonData['disk']['total']}G"
    if jsonData['gpu']['temp']:
        gpu_temp.text = f"{jsonData['gpu']['temp']} °C"
    else:
        gpu_temp.text = ".. °C"

while True:
    if supervisor.runtime.serial_bytes_available: # If new serial data
        handleSerial()

    # When the display is touched
    touch = ts.touch_point
    if touch:
        if detailed:
            detailed = False
            hideLayer(detailView)
            toggle_label.text = "Basic"
            toggle_label.x = 270
        else:
            detailed = True
            showLayer(detailView)
            toggle_label.text = "Detailed"
            toggle_label.x = 250
        while ts.touch_point:
            pass
