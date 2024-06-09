import serial
from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory=".")

# Abrir la conexión serial
ser = serial.Serial('/dev/ttyACM0', 9600)  # Modifica el puerto y la velocidad según tus necesidades

# Función para leer datos del puerto serial
def read_serial_data():
    # Lee los datos del puerto serial
    data = ser.readline().decode().strip()  # Decodifica y elimina espacios en blanco
    return data

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    # Renderizar el HTML contenido en este mismo archivo
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta WebSocket para enviar datos del puerto serial al cliente
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Leer datos del puerto serial
        data = read_serial_data()
        if data:
            await websocket.send_text(data)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
