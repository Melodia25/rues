import json
from datetime import datetime
import httpx
import os
from rich import print
timeout: int = 15
headers = {
    'authority': 'pruebasruesapi.rues.org.co',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://ruesdevext.rues.org.co',
    'referer': 'https://ruesdevext.rues.org.co/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}
def save_dict_to_json(data_dict: dict, file_name: str) -> None:
    directory = "data"
    sub_directories = ["nit"]

    # Comprobar si el directorio existe, si no, crearlo
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Comprobar si los subdirectories existen
    for folder in sub_directories:
        sub_directory_path = os.path.join(directory, folder)
        if not os.path.exists(sub_directory_path):
            os.makedirs(sub_directory_path)

    # Ruta completa del archivo
    file_path = os.path.join(directory, file_name)

    with open(file_path, 'w') as file:
        json.dump(data_dict, file)
def read_token():
    file_name = "data/token.json"

    try:
        # Intenta leer el archivo json de token
        with open(file_name) as archivo:
            data = json.load(archivo)
        return data
    except FileNotFoundError:
        # Si el archivo no existe, retorna None
        print(f"The file '{file_name}' does not exist.")
        return None


def is_token_valid():
    # Formato de fecha correspondiente
    format_date = "%a, %d %b %Y %H:%M:%S %Z"

    # Obtener la fecha de expiración del archivo
    data = read_token()
    if not data:
        return False

    expires_str = data[".expires"]
    expiration_date = datetime.strptime(expires_str, format_date)

    # Obtener la fecha y hora actual
    current_date = datetime.now()

    # Comparar la fecha actual con la fecha de expiración
    return current_date < expiration_date


def obtain_token() -> str:
    url: str = "https://pruebasruesapi.rues.org.co/token"

    payload: dict = {
        "grant_type": "password",
        "username": "SIIUser",
        "password": "Webapi2017*"
    }

    # if is_token_valid():
    #     data = read_token()
    #     return data['access_token']

    with httpx.Client(timeout=timeout) as client:
        response = client.post(url=url, data=payload, headers=headers)
        if response.status_code == 200:
            save_dict_to_json(response.json(), 'token.json')
            return response.json()['access_token']
        else:
            print(f"Error: {response.status_code}")
            return None


def consulta_nit(nit: str):
    url: str = 'https://pruebasruesapi.rues.org.co/api/ConsultasRUES/ConsultaNIT'
    params = {
        'usuario': 'SIIUser',
        'nit': nit,
    }
    token = obtain_token()

    try:

        with httpx.Client(timeout=timeout) as client:
            headers["authorization"] = f"Bearer {token}"
            response = client.post(url=url, params=params, headers=headers)
            if response.status_code == 200:
                values = response.json()
                return values
            else:
                raise Exception(
                    f"Error - Consulta NIT: {response.status_code}")
    except Exception as e:
        # print(f"{e}")
        return None

def consulta_matricula(cod_camara: str, matricula: str):
    # api/ConsultasRUES/ConsultaMatricula
    url: str = 'https://pruebasruesapi.rues.org.co/api/ConsultasRUES/ConsultaMatricula'
    params = {
        'usuario': 'SIIUser',
        'codCam': cod_camara,
        'mat': matricula
    }
    token = obtain_token()

    with httpx.Client() as client:
        headers["authorization"] = f"Bearer {token}"
        response = client.post(url=url, params=params, headers=headers)
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
