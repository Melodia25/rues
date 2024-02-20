import pandas as pd
import numpy as np
import json
import ijson
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

# Este script realiza el preprocesamiento y estructuración de la base de datos

# Preprocesamiento

df_rues = pd.read_csv("RUES/901235691_18-10-2022 10_53_20_ok.CSV", sep=',', encoding='latin-1')
df_rues['numero_identificacion'] = df_rues['numero_identificacion'].astype('str')
df_rues['fecha_matricula'] = pd.to_datetime(df_rues['fecha_matricula']).dt.strftime('%d/%m/%Y')

# Eliminación de registros duplicados
df_rues.sort_values(by=['numero_identificacion', 'fecha_matricula'], inplace=True)
df_rues.drop_duplicates(subset=['numero_identificacion', 'municipio'], keep='first', inplace=True)
df_rues.sort_index(inplace=True)


# Información de Registro Mercantil (RUES)
def read_json_rues(rues_file='RUES/rues2022_complementaria.json'):
    # Esta función lee y procesa data del registro mercantil RUES
    # JSON con información acerca del estado y número de matrícula, tipo de sociedad, fechas y establecimientos
    data = {}

    with open(rues_file, "rb") as f:
        for record in ijson.items(f, "item"):
            empresa = record["empresa"]["nit"]
            fecha_rues = record["fecha"]["$date"]
            estado = record["empresa"]["estado"]
            numero_matricula = record["empresa"]["registro_mercantil"]["numero_de_matricula"]
            tipo_organizacion = record["empresa"]["registro_mercantil"]["tipo_de_organización"]
            try:
                tipo_sociedad = record["empresa"]["registro_mercantil"]["tipo_de_sociedad"]
            except:
                continue

            data[empresa] = []
            data[empresa].append(fecha_rues)
            data[empresa].append(estado)
            data[empresa].append(numero_matricula)
            data[empresa].append(tipo_organizacion)
            data[empresa].append(tipo_sociedad)

    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['nit', 'fecha_rues', 'estado', 'numero_matricula', 'tipo_organizacion', 'tipo_sociedad']
    df['nit'] = df['nit'].astype('str')
    df['fecha_rues'] = pd.to_datetime(df['fecha_rues']).dt.strftime("%d/%m/%Y")

    return df


def json_linebyline(rues_file="RUES/test.json"):
    # Lectura de archivo JSON cuando posee una estructura JSON línea por línea
    dict = {"nit": [], "fecha_rues": []}

    df_list = []
    with open(rues_file, 'r', encoding='utf8') as json_file:
        for line in json_file:
            # Read each line as json object
            data = json.loads(line.strip()[:-1])

            dict["nit"].append(data[0]['nit'])

            date_unix = int(data[0]['fecha']['$date'])/1000
            dict["fecha_rues"].append(datetime.utcfromtimestamp(date_unix).strftime('%d/%m/%Y'))

            data_empresa = data[0]['empresa']
            df_list.append(data_empresa)

    # Extracción de información de matrícula registrada en diccionario anidado
    df_empresa = pd.DataFrame(df_list)
    df_empresa['nit'] = df_empresa['nit'].astype('str')
    df_empresa = pd.concat(objs=[df_empresa[['nit', 'estado']],
                                 df_empresa['registro_mercantil'].apply(pd.Series)[['numero_de_matricula', 'tipo_de_organización', 'tipo_de_sociedad']]],
                                 axis=1)

    df_nit = pd.DataFrame(dict)
    df_nit['nit'] = df_nit['nit'].astype('str')

    df = pd.merge(df_nit, df_empresa, on='nit')

    # Para los registros anteriores al 2021 se eilima el estado de la empresa y la fecha, esto por falta de precisión en la información
    df.loc[pd.to_datetime(df['fecha_rues']).dt.year < 2022, 'estado'] = ''
    df.loc[pd.to_datetime(df['fecha_rues']).dt.year < 2022, 'fecha_rues'] = ''

    df.drop_duplicates(subset=['nit'], inplace=True)
    df.columns = ['nit', 'fecha_rues', 'estado', 'numero_matricula', 'tipo_organizacion', 'tipo_sociedad']

    return df


# Datos Registro Mercantil
df_estado = read_json_rues('RUES/rues2022_complementaria.json')
df_faltantes = json_linebyline('RUES/test.json')

df_registromerc = pd.concat(objs=[df_estado, df_faltantes])

# Integración de la información del registro mercantil
df_rues['fecha_rues'] = df_rues['numero_identificacion'].map( dict(zip(df_estado.nit, df_estado.fecha_rues)) )
df_rues['estado'] = df_rues['numero_identificacion'].map( pd.Series(data=df_estado['estado'].values, index=df_estado['nit']) )
df_rues['numero_matricula'] = df_rues['numero_identificacion'].map( pd.Series(data=df_estado['numero_matricula'].values, index=df_estado['nit']) )
df_rues['tipo_organizacion'] = df_rues['numero_identificacion'].map( pd.Series(data=df_estado['tipo_organizacion'].values, index=df_estado['nit']) )
df_rues['tipo_sociedad'] = df_rues['numero_identificacion'].map( pd.Series(data=df_estado['tipo_sociedad'].values, index=df_estado['nit']) )

# Sectores económicos, actividad económica, CIIU y subdivisiones

# Información de clasificación por el nuevo sector económico propuesto por Td
sector = pd.read_excel('Segmentador/Macrosectores_Keywords.xlsx')

for i in range(len(sector['KEYWORDS'])):
    sector['KEYWORDS'][i] = sector['KEYWORDS'][i].split(';')

df_rues['sector_economico']= np.full((len(df_rues),1), 'False')
for i in range(len(sector['MACROSECTOR'])):
    for j in range(len(sector['KEYWORDS'][i])):
        keyword = sector['KEYWORDS'][i][j]
        df_rues['boolean'] = df_rues['actividad_economica'].str.contains(' '+keyword) | df_rues['actividad_economica'].str.lower().str.startswith(keyword)
        df_rues['sector_economico'][df_rues['boolean'] == True] = sector['MACROSECTOR'][i]

df_rues['sector_economico'] = df_rues['sector_economico'].replace('False', np.nan)

df_rues = df_rues.drop(['boolean'], axis=1)