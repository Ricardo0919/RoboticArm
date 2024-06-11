import serial
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from ultrasonico import measure_distance
#from sensor import SensorValues 

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para la página de datos del sensor
@app.get("/serial_data.html", response_class=HTMLResponse)
async def main(request: Request):
    # Renderizar el HTML contenido en este mismo archivo
    distancia = measure_distance()
    if distancia<=30:
        return templates.TemplateResponse("serial_data.html", {"request": request, "distancia": distancia})
    if distancia>30:
        return templates.TemplateResponse("serial_data.html", {"request": request, "distancia": "Not in range"})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)