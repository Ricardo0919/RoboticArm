import RPi.GPIO as GPIO
import time

def measure_distance():
    TRIG = 40
    ECHO = 38

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    GPIO.output(TRIG, False)
    # print("Calibrando.....")
    # time.sleep(2)
    # print("Objeto muy alejado......")
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        inicio_pulso = time.time()

    while GPIO.input(ECHO) == 1:
        fin_pulso = time.time()

    duracion_pulso = fin_pulso - inicio_pulso
    distancia = duracion_pulso * 17150
    distancia = round(distancia + 1.15, 2)
    
    GPIO.cleanup()
    
    return distancia


# while True:
#     distancia = measure_distance()
#     if distancia <= 20:
#         print("distancia:", distancia, "cm")
#     if distancia > 20:
#         print("Objeto muy alejado....")
#     time.sleep(2)

