import tkinter as tk
from tkinter import Button, Frame, Tk
from tkinter.ttk import Combobox, Style

from motors_serial import BAUDRATES
from motors_serial import SensorSerial
from utils import find_available_serial_ports
import threading
import socket

class App(Frame):
    def __init__(self, master, *args, **kwargs) -> None:
        Frame.__init__(self, master, *args, **kwargs)
        self.master: Tk = master

        # GUI objects creations
        self.serial_devices_combobox: Combobox = self.create_serial_devices_combobox()
        self.refresh_serial_devices_button: Button = self.create_serial_devices_refresh_button()
        self.baudrate_combobox: Combobox = self.create_baudrate_combobox()
        self.connect_serial_button: Button = self.create_connect_serial_button()
        self.send_buttons = self.create_send_buttons()
        self.continue_sending = False  # Flag to control continuous sending
        self.sending_thread = None  # Thread for sending characters

        self.init_gui()
        # Other objects
        self.sensor_serial: SensorSerial | None = None

    def init_gui(self) -> None:
        # GUI Config
        self.master.title('Serial Communication')
        self.master.geometry('400x500')
        self['bg'] = '#000000'  # Set background to black
        self.pack(fill='both', expand=True, padx=20, pady=20)

        # Center the window on the screen
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

        # Style Config
        style = Style()
        style.configure('TCombobox', fieldbackground='#000000', background='#000000', foreground='white')

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        for i in range(4, 9):
            self.grid_rowconfigure(i, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.refresh_serial_devices_button.grid(row=0, column=0, pady=10, padx=12, columnspan=2, sticky='nsew')
        self.serial_devices_combobox.grid(row=1, column=0, pady=10, padx=12, columnspan=2, sticky='nsew')
        self.connect_serial_button.grid(row=2, column=0, pady=10, padx=12, columnspan=2, sticky='nsew')

        for idx, (d_button, l_button) in enumerate(self.send_buttons, start=4):
            d_button.grid(row=idx, column=0, pady=5, padx=5, sticky='nsew')
            l_button.grid(row=idx, column=1, pady=5, padx=5, sticky='nsew')

        # Settings
        self.baudrate_combobox.current(0)

    def create_serial_devices_combobox(self) -> Combobox:
        ports = find_available_serial_ports()
        return Combobox(self, values=ports, font=('Courier', 12), style='TCombobox')

    def create_serial_devices_refresh_button(self) -> Button:
        return Button(self,
                      text='Refresh Serial Devices',
                      command=self.refresh_serial_devices,
                      bg='#000000', fg='white'
                      )

    def create_baudrate_combobox(self) -> Combobox:
        return Combobox(self, values=BAUDRATES, font=('Arial', 12), style='TCombobox')

    def create_connect_serial_button(self) -> Button:
        return Button(self, text='Connect', bg='#ffd700', fg='black', command=self.create_sensor_serial)

    def create_send_buttons(self):
        button_commands = [
            ('D1', 'q'), ('D2', 'w'), ('D3', 'e'), ('D4', 'r'),
            ('L1', 'y'), ('L2', 'u'), ('L3', 'i'), ('L4', 'o')
        ]
        buttons = []
        for d_text, char in button_commands[:4]:
            d_button = Button(self, text=d_text, bg='#ffd700', fg='black')
            d_button.bind('<ButtonPress>', lambda e, c=char: self.start_sending(c))
            d_button.bind('<ButtonRelease>', lambda e: self.stop_sending())
            buttons.append(d_button)

        for l_text, char in button_commands[4:]:
            l_button = Button(self, text=l_text, bg='#ffd700', fg='black')
            l_button.bind('<ButtonPress>', lambda e, c=char: self.start_sending(c))
            l_button.bind('<ButtonRelease>', lambda e: self.stop_sending())
            buttons.append(l_button)
        
        return [(buttons[i], buttons[i+4]) for i in range(4)]

    def refresh_serial_devices(self):
        ports = find_available_serial_ports()
        self.serial_devices_combobox['values'] = ports
        self.serial_devices_combobox.set('')

    def create_sensor_serial(self) -> SensorSerial:
        port = self.serial_devices_combobox.get()
        baudrate = self.baudrate_combobox.get()

        # Create a thread to handle socket connection
        threading.Thread(target=self.send_status_to_server, args=(port, baudrate)).start()

    def send_status_to_server(self, port, baudrate):
        app_socket = socket.socket()
        app_socket.connect(('localhost', 8000))

        if not port or not baudrate.isdigit():
            app_socket.send(b"Sin conexion")
            app_socket.close()
            raise ValueError(f'Incorrect values for port: {port}, baudrate: {baudrate}')

        app_socket.send(b"Dispositivo conectado")
        app_socket.close()
        self.sensor_serial = SensorSerial(serial_port=port, baudrate=int(baudrate))

    def start_sending(self, char: str) -> None:
        if self.sensor_serial is not None:
            self.continue_sending = True
            self.sending_thread = threading.Thread(target=self.send_char_continuously, args=(char,))
            self.sending_thread.start()
        else:
            raise RuntimeError('Serial connection has not been initialized')

    def stop_sending(self) -> None:
        self.continue_sending = False
        if self.sending_thread is not None:
            self.sending_thread.join()
            self.sending_thread = None

    def send_char_continuously(self, char: str) -> None:
        while self.continue_sending:
            self.sensor_serial.send(char.lower())


root = Tk()

if __name__ == '__main__':
    app = App(root)
    root.mainloop()
