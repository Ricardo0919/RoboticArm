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

status = "Sin Status"
last_message_time = None

async def handle_client(reader, writer):
    global status, last_message_time
    data = await reader.read(1024)
    status = data.decode('utf-8')
    last_message_time = asyncio.get_event_loop().time()  # Registrar la última vez que se recibió un mensaje
    writer.close()
    await writer.wait_closed()

async def start_socket_server():
    server = await asyncio.start_server(handle_client, 'localhost', 8000)
    async with server:
        await server.serve_forever()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_socket_server())
    asyncio.create_task(reset_status_if_no_message())

async def reset_status_if_no_message():
    global status, last_message_time
    while True:
        await asyncio.sleep(10)  # Verificar cada 10 segundos
        if last_message_time is not None:
            elapsed_time = asyncio.get_event_loop().time() - last_message_time
            if elapsed_time > 10:  # Si han pasado más de 10 segundos sin recibir un mensaje
                status = "Sin status"
                last_message_time = None

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
