import serial
import time

# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyAMA0',  # Replace with your serial port
    baudrate=9600,
    timeout=1
)


def send_command(cmd):
    ser.write(cmd.encode('utf-8'))
    time.sleep(0.2)


def forward():
    send_command("w\n")


def backward():
    send_command("s\n")


def left():
    send_command("a\n")


def right():
    send_command("d\n")


def stop():
    send_command("stop\n")


# Main program
try:
    while True:
        # Here you can add your logic to decide which command to send
        # Example: forward for 2 seconds, then stop
        forward()
        time.sleep(2)
        stop()
        time.sleep(2)

except KeyboardInterrupt:
    # Gracefully stop the motors on KeyboardInterrupt
    stop()
    ser.close()
