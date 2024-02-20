import pandas as pd
import typer
from rues import consulta_nit, consulta_matricula
from rich import print
from rich.progress import track
import pandas as pd
import time

from builder import Builder
from elasticsearch import Elasticsearch
app = typer.Typer()
import json

es = Elasticsearch("http://localhost:9200")
def update_state(filename_csv: str, nit: str, state: str):
    # Leer el archivo CSV
    df = pd.read_csv(filename_csv)

    # Obtener el NIT y cambiar el estado a "revisado"
    df.loc[df['NIT'] == nit, 'ESTADO'] = state

    # Guardar el DataFrame actualizado en el mismo archivo CSV
    df.to_csv(filename_csv, index=False)

@app.command("process")
def process_nit( file_name:str="lista_nit.csv"):
    df = pd.read_csv(file_name)
    df = df[df["ESTADO"]=="pendiente"]
    lista_nit = df["NIT"].tolist()[0:5000]
    total =len(lista_nit) - 1
    resultado = []
    errores = []
    place = 0

    for i in track(lista_nit, description="Consultando nit.."):
        place = place +1
        print(f"[green]Procesando el nit [bold red]{i}  [green]posicion actual [bright_cyan]{place} de {total}")
        response = consulta_nit(i)
        try:
            build = Builder(response)
            es.index(index="rues_news", document=build.get_data)
            if build.get_data != {}:
                update_state(file_name, i, 'revisado')
            print(f"[green]actualizando  el nit [bold red]{i} [green]en el archivo")
            time.sleep(1)
            if place % 100 == 0:
                time.sleep(10)
        except Exception as e:
            print(f"El nit [bold red]{i} [green] No se pudo procesar")

            errores.append(i)



    #
    # with open('data/rues_data.json', 'w') as archivo_json:
    #     json.dump(resultado, archivo_json, indent=4)

    print("Los siguientes archivos tuvieron erroes")
    print(errores)
# @app.command("delete")
# def process_nit_b(nit: str):
#     a = consulta_nit(nit)
#     print(a)

if __name__ == "__main__":
    app()

