//  Alumnos:
//  José Ángel Huerta Rios A01710707
//  Ezzat Alzahouri Campos A01710709
//  Ricardo Sierra Roa A01709887
//  Diseño de Sistemas en chip
//  Control de Servos con Serial y teclado capacitivo
//  Instituto Tecnológico y de Estudios Superiores de Monterrey, 
//  Campus Querétaro

#include <Wire.h>
#include "Adafruit_MPR121.h"
#include <Servo.h>

// Crear objetos Servo para cada uno de los servos
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

// Pines a los que están conectados los servos
int servoPin1 = 8;
int servoPin2 = 9;
int servoPin3 = 11;
int servoPin4 = 10;

// Ángulos iniciales de los servos
int currentAngle1 = 90;
int currentAngle2 = 90;
int currentAngle3 = 90;
int currentAngle4 = 90;

// Crear una instancia del sensor capacitivo
Adafruit_MPR121 cap = Adafruit_MPR121();

void setup() {
  // Asigna los pines a los servos
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo3.attach(servoPin3);
  servo4.attach(servoPin4);

  // Inicializa la comunicación serial
  Serial.begin(9600);

  // Mueve los servos a los ángulos iniciales
  servo1.write(currentAngle1);
  servo2.write(currentAngle2);
  servo3.write(currentAngle3);
  servo4.write(currentAngle4);

  // Inicializar el sensor capacitivo
  if (!cap.begin(0x5A)) {  // La dirección I2C predeterminada para el MPR121 es 0x5A
    while (1);
  }
}

void loop() {
  // Verifica si hay datos disponibles en el puerto serial
  if (Serial.available()) {
    // Lee el carácter del puerto serial
    char command = Serial.read();
    processCommand(command);
  }

  // Leer el estado de los sensores del MPR121
  uint16_t touched = cap.touched();

  // Botón 4 (q)
  if (touched & (1 << 4)) {
    processCommand('q');
  }
  // Botón 8 (y)
  if (touched & (1 << 8)) {
    processCommand('y');
  }
  // Botón 5 (w)
  if (touched & (1 << 5)) {
    processCommand('w');
  }
  // Botón 9 (u)
  if (touched & (1 << 9)) {
    processCommand('u');
  }
  // Botón 6 (e)
  if (touched & (1 << 6)) {
    processCommand('e');
  }
  // Botón 10 (i)
  if (touched & (1 << 10)) {
    processCommand('i');
  }
  // Botón 7 (r)
  if (touched & (1 << 7)) {
    processCommand('r');
  }
  // Botón 11 (o)
  if (touched & (1 << 11)) {
    processCommand('o');
  }

  delay(100);  // Pequeña demora para evitar múltiples detecciones rápidas
  Serial.print(currentAngle1);
  Serial.print(",");
  Serial.print(currentAngle2);
  Serial.print(",");
  Serial.print(currentAngle3);
  Serial.print(",");
  Serial.println(currentAngle4);
}

void processCommand(char command) {
  // Incrementa o decrementa el ángulo basado en el comando recibido
  switch (command) {
    case 'q':
      currentAngle1 += 10;
      if (currentAngle1 > 180) currentAngle1 = 180;
      servo1.write(currentAngle1);
      break;
      
    case 'y':
      currentAngle1 -= 10;
      if (currentAngle1 < 0) currentAngle1 = 0;
      servo1.write(currentAngle1);
      break;
      
    case 'w':
      currentAngle2 += 10;
      if (currentAngle2 > 180) currentAngle2 = 180;
      servo2.write(currentAngle2);
      break;
      
    case 'u':
      currentAngle2 -= 10;
      if (currentAngle2 < 0) currentAngle2 = 0;
      servo2.write(currentAngle2);
      break;
             
    case 'e':
      currentAngle3 += 10;
      if (currentAngle3 > 180) currentAngle3 = 180;
      servo3.write(currentAngle3);
      break;
      
    case 'i':
      currentAngle3 -= 10;
      if (currentAngle3 < 0) currentAngle3 = 0;
      servo3.write(currentAngle3);
      break;
    
    case 'r':
      currentAngle4 += 10;
      if (currentAngle4 > 180) currentAngle4 = 180;
      servo4.write(currentAngle4);
      break;
      
    case 'o':
      currentAngle4 -= 10;
      if (currentAngle4 < 0) currentAngle4 = 0;
      servo4.write(currentAngle4);
      break;
      
    default:
      break;
  }
}
