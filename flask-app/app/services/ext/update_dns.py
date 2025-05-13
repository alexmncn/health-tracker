import sys
import os
import socket
import base64
import requests

# Añadir la raíz del proyecto al sys.path
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(app_path)

from app.services.pushover_alerts import send_alert
from app.config import NOIP_DNS


def get_server_ip():
    response = requests.get('https://api.ipify.org?format=json', timeout=10)
    return response.json()['ip']


def get_dns_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        raise Exception(f"No se pudo resolver el dominio {hostname}: {e}")


def make_get_request(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.status_code, response
        else:
            return response.status_code, f'Error {response.status_code}: {response.reason}'
    except Exception as e:
        return None, f'Error en la solicitud: {e}'


def update_ip_dns(new_ip):
    url = NOIP_DNS.URL
    params = {
        'myip': new_ip,
        'hostname': NOIP_DNS.HOSTNAME,
    }

    auth_str = f"{NOIP_DNS.USERNAME}:{NOIP_DNS.PASSWORD}"
    auth_bytes = auth_str.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth_str = base64_bytes.decode('ascii')

    headers = {
        'User-Agent': 'Python-Client/1.0',
        'Authorization': f'Basic {base64_auth_str}'
    }

    code, response = make_get_request(url, params=params, headers=headers)

    if code == 200:
        body = response.text.strip()
        if body.startswith("good "):
            return "updated"
        elif body.startswith("nochg "):
            return "nochange"
        else:
            raise Exception(f"Respuesta inesperada: {body}")
    elif code == 401:
        raise Exception("Credenciales inválidas")
    else:
        raise Exception(f"Error HTTP: {response}")


def main():
    try:
        public_ip = get_server_ip()
        dns_ip = get_dns_ip(NOIP_DNS.HOSTNAME)

        if public_ip == dns_ip:
            return

        send_alert(f'La IP del servidor ha cambiado a {public_ip}. Actualizando...', -1)

        result = update_ip_dns(public_ip)
        if result == "updated":
            send_alert('Se ha actualizado la IP en No-IP.', -1)
        elif result == "nochange":
            send_alert('La IP ya estaba actualizada en No-IP.', -1)

    except Exception as e:
        send_alert(f'Error al actualizar IP en No-IP: {e}', 0)


if __name__ == "__main__":
    main()
