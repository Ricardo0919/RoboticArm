import sys
import serial
import serial.tools.list_ports
import glob

def find_available_serial_ports() -> list[str]:
    if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
        # Para Windows y macOS
        ports = serial.tools.list_ports.comports()
        result = [port.device for port in ports]

    elif sys.platform.startswith('linux'):  # Computadora Linux
        # Para Linux
        ports = serial.tools.list_ports.comports()
        result = [port.device for port in ports]
        return result
    
    elif sys.platform.startswith('darwin'):  # Mac
        ports = glob.glob('/dev/tty.*')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                continue

    else:
        raise EnvironmentError('Unsupported Platform')

    return result

if __name__ == '__main__':
    # Ejemplo de uso:
    available_ports = find_available_serial_ports()
    print("Available ports:", available_ports)
