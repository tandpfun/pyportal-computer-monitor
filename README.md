# PyPortal Computer Monitor
See your computer's CPU usage, RAM usage, GPU usage, and disk usage on your PyPortal display!

> Note: This is mostly only compatible with Windows, and stuff might not work. I'm not great at python, but if anyone else knows how to create better compatibility, create a PR!

(Images Here)

## How it works:
To get the data from your computer to the display, this project uses Serial. On your computer, a python file is running and monitoring your computer and sending the data over to the PyPortal over Serial. The python file does need to be running on your computer at all times for it to work, though.

## Setup:
1. First, clone the repository over to your computer. The code files for both the PyPortal and your computer are located in the src file.
2. Move the images, fonts, and code.py file over into your pyportal.
3. Next, you are going to want to get the required libraries for this file and put them into your `/lib/` file on your PyPortal. Here are the required libraries:
> * adafruit_bitmap_font
> * adafruit_display_text
> * adafruit_touchscreen

4. At this point, your PyPortal should work and the display should show the labels, but no numbers yet. To do this, we're going to have to use a python script running on your computer.
5. First, install the pip packages. Here's what you need:
> * `pip3 install pyserial`
> * `pip3 install psutil`
> * `pip3 install shutil`
> * `pip3 install GPUtil`

6. Then, at the top of the sendData.py file, change the `DEVICE` variable to the device's USB port. On windows, this looks like `COM5`. On mac, this looks like `dev/tty.devicename`. Use google to figure out how to find this device if you do not know which one it is.
7. Now, start the file with `python3 /path/to/file/sendData.py`. If all is working, you should see data displayed on your PyPortal! If not feel free to open an issue, or fix an issue yourself with a PR.


Thanks for checking out the project!
