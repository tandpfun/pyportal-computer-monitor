import time
import serial
import psutil
import shutil
import GPUtil

# MAC: DEVICE = 'dev/tty.devicename'
# WINDOWS: Device = 'COM(port here)'
DEVICE = 'COM5'

count = 0 # to see how many times data has been sent
while True:
    count = count+1
    ser = serial.Serial(DEVICE, 115200)  # open serial port

    # CPU Stats
    cpu_percent = str(psutil.cpu_percent(interval=1)) # Get CPU percent (Takes 1 second)
    cpu_temp = "..." # Haven't figured out how to get CPU temp yet

    # RAM Stats
    ram_percent = str(psutil.virtual_memory().percent)
    ram_used = str(round(psutil.virtual_memory().used / (2**30), 1))
    ram_total = str(round(psutil.virtual_memory().total / (2**30), 1))

    # Get GPU Stats (Windows Only)
    if GPUtil.getGPUs():
        gpu_percent = f"{round(GPUtil.getGPUs()[0].load*100, 2)}"
        gpu_temp = f"{GPUtil.getGPUs()[0].temperature}"
    else:
        gpu_percent = ""
        gpu_temp = ""

    # Get Disk Stats
    storage_total, storage_used, storage_free = shutil.disk_usage("/")
    disk_percent = str(round((storage_used / (2**30)) / (storage_total / (2**30))*100, 1))
    disk_total = str(round(storage_total / (2**30)))
    disk_used = str(round(storage_used / (2**30)))

    # Create JSON Data
    command = '{"cpu":{"percent": "'+ cpu_percent +'", "temp": "'+ cpu_temp +'"},"ram":{"percent": "'+ ram_percent +'", "used":"'+ ram_used +'", "total":"'+ ram_total +'"},"gpu":{"percent":"'+ gpu_percent +'", "temp":"'+ gpu_temp +'"},"disk":{"percent":"'+ disk_percent +'","used":"'+ disk_used +'","total":"'+ disk_total +'"}}\n\r'
    command = command.encode('utf-8') # Format the data
    
    print(f"Sending Data... | x{count}", end="\r")
    ser.write(command) # Write a string to the serial

    ended = False
    reply = b''

    # Read Response
    for _ in range(len(command)):
        a = ser.read()

    while True:
        a = ser.read()

        if a== b'\r':
            break

        else:
            reply += a

        time.sleep(0.01)

    print(f"Sending Data ✓  | x{count}", end="\r")

    ser.close()
