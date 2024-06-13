# Robot Arm

## Tabla de Contenidos

- [Descripción](#descripción)
- [Componentes y Funcionalidades](#componentes-y-funcionalidades)
- [Instalación](#instalación)
- [Uso](#uso)

## Descripción

Este proyecto se centra en la creación y programación de una aplicación en Python para controlar un brazo robótico utilizando un Arduino, alojada en un servidor web ejecutado en una Raspberry Pi 4. La aplicación permite a los usuarios ajustar y manipular los ángulos de los diferentes segmentos del brazo robótico, facilitando la ejecución de tareas complejas con alta precisión.

## Componentes y Funcionalidades

1. **Control del Brazo Robótico**
   - **Teclado Capacitivo:** Permite el control local de los ángulos y movimientos del brazo robótico en cualquiera de sus articulaciones(4 servos), por medio de un Arduino uno el cual esta conectado por el puerto serial a la Raspberry Pi 4(servidor).
   - **Aplicación Python con Tkinter:** Proporciona una interfaz gráfica remota para controlar los ángulos del brazo robótico en cualquiera de sus articulaciones(4 servos) desde la Raspberry Pi 4 conectada al Arduino por puerto serial.

2. **Sensor de Proximidad Ultrasónico**
   - **Medición en Tiempo Real:** Utiliza un sensor ultrasónico para medir distancias en tiempo real, crucial para la operación precisa del brazo robótico en entornos dinámicos.
   - **Visualización de Datos:** Los datos del sensor se muestran en una interfaz web que se actualiza cada segundo mediante un iframe, ofreciendo a los usuarios una monitorización continua y precisa de las proximidades del brazo robótico.

3. **Servidor Web con FastAPI**
   - **Interfaz Web:** El servidor web, construido con FastAPI y alojado en la Raspberry Pi 4, presenta los datos del sensor de proximidad de forma dinámica.
   - **Actualización en Tiempo Real:** Un iframe en la página web se recarga cada segundo para reflejar los valores actuales del sensor de proximidad.
   - **Botón de Acceso Rápido:** Incluye un botón en la interfaz web que permite abrir la aplicación Tkinter en la Raspberry Pi, facilitando un control remoto eficiente del brazo robótico.

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- FastAPI
- Uvicorn
- Tkinter
- asyncio

### Instrucciones

1. Clona el repositorio:

    ```bash
    git clone https://github.com/RicardoSR19/RoboticArm.git
    cd RoboticArm/
    ```

2. Crea un entorno virtual:

    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Iniciar el servidor

Para iniciar el servidor que recibe y muestra datos del brazo robótico:

```bash
    python main.py
```

### Iniciar la aplicacion 

Para iniciar la aplicacion en la raspberry(RealVNC o pantalla para visualizar la app):

```bash
    python app.py
```

Desde la aplicación podras conectarte al puerto serial del arduino y poder mover de manera remota los angulos de las articulaciones del robot.

### Resultados web

Para visualizar los resultados y datos del web server necesitaras acceder en un navegador a `http://localhost:8080`


