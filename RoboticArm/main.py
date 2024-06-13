from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio

from ultrasonico import measure_distance

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

status = "La aplicacion no esta ejecutada"

async def handle_client(reader, writer):
    global status
    data = await reader.read(1024)
    status = data.decode('utf-8')
    writer.close()
    await writer.wait_closed()

async def start_socket_server():
    server = await asyncio.start_server(handle_client, 'localhost', 8000)
    async with server:
        await server.serve_forever()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_socket_server())

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para la página de datos del sensor
@app.get("/serial_data.html", response_class=HTMLResponse)
async def serial_data(request: Request):
    distancia = measure_distance()
    distancia_text = distancia if distancia <= 30 else "Not in range"
    return templates.TemplateResponse("serial_data.html", {"request": request, "distancia": distancia_text, "status": status})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
