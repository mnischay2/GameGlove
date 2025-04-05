import sys
import serial
SERIAL_PORT = "COM4"  # Change as needed
BAUD_RATE = 9600
def read_esp32():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                if ser.in_waiting:
                    data= str(ser.readline().decode('latin-1', 'ignore').strip())
                    print("Received:", data) 
    except serial.SerialException as e:
        print("Error:", e)
        sys.exit(1)
while True:
    read_esp32()