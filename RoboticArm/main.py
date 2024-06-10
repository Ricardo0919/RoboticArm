import serial
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Correct directory path

# Abrir la conexión serial
ser = serial.Serial('/dev/ttyACM0', 9600)  # Modifica el puerto y la velocidad según tus necesidades

# Función para leer datos del puerto serial
def read_serial_data():
    data = ser.readline().decode().strip()  # Decodifica y elimina espacios en blanco
    print(data)
    return data

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para obtener los datos seriales

@app.get("/serial_data.html", response_class=HTMLResponse)
async def get_serial_data(request: Request):
    data = read_serial_data()
    return templates.TemplateResponse("serial_data.html", {"request": request, "data": data})



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
