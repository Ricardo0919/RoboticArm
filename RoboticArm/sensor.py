import RPi.GPIO as GPIO
import dht11
import time

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()  # Uncomment this line if you need to clean up GPIO settings

# Read data using Pin GPIO4 (you can change it back to GPIO21 if needed)
instance = dht11.DHT11(pin=21)

def SensorValues():
    result = instance.read()
    temperature = result.temperature
    humidity = result.humidity
    return temperature, humidity

# while True:
#     print("Reading sensor data...")  # Debug print
#     temperature, humidity = SensorValues()
#     print(f"Temp: {temperature} C Humid: {humidity} %")
#     time.sleep(1)
