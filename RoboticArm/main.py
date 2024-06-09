import serial
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory=".")

# Importando funciones y clases de los archivos externos
from motors_serial import BAUDRATES, SensorSerial
from utils import find_available_serial_ports

# Función para leer datos del puerto serial
def read_serial_data():
    # Abre la conexión serial (asegúrate de que el puerto serial y la velocidad coincidan)
    ser = serial.Serial('/dev/ttyS0', 9600)  # Modifica el puerto y la velocidad según tus necesidades

    # Lee los datos del puerto serial
    data = ser.readline().decode().strip()  # Decodifica y elimina espacios en blanco
    ser.close()  # Cierra la conexión serial
    return data

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    # Renderiza el HTML contenido en este mismo archivo
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

# Ruta para procesar los datos del puerto serial
@app.post("/upload_data/")
async def upload_data(angle_data: str = Form(...)):
    # Aquí puedes procesar los datos recibidos como sea necesario
    print("Datos recibidos del puerto serial:", angle_data)
    return {"message": "Datos recibidos correctamente"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
