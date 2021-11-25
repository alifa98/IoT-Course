import serial


with serial.Serial('/dev/ttyUSB0', 115200) as serialInput:
    while True:
        print(serialInput.readline().decode())

        # you can cal a function to do something with the request
        # like send it to the server or pause the video or ...
        # Note 1: the request is a string
        # Note 2: function call should run on another thread (Use Future feature)
