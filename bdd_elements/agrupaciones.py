import sqlite3
import pandas as pd


def calcular_info_por_agrupacion(data):
    num_observaciones = data.count()
    num_valores_ausentes = data.isnull().sum()
    mediana = data.median()
    media = data.mean()
    varianza = data.var()
    maximo = data.max()
    minimo = data.min()
    return num_observaciones, num_valores_ausentes, mediana, media, varianza, maximo, minimo

def get_group_by_type(ruta):
    con = sqlite3.connect(f"{ruta}/gicib_SI_practica1_sistemaETL.db")
    query = '''
            SELECT *
            FROM usuarios
            '''
    df = pd.read_sql_query(query, con)
    con.close()
    return df.groupby('permisos')

def get_group_by_pwd_strength(ruta):
    con = sqlite3.connect(f"{ruta}/gicib_SI_practica1_sistemaETL.db")
    query = '''
            SELECT *
            FROM usuarios
            '''
    df = pd.read_sql_query(query, con)
    con.close()
    return df.groupby('pwd_debil')


def init(ruta):
    keys = ["num_observaciones", "num_valores_ausentes", "mediana", "media", "varianza", "maximo", "minimo"]

    info_user = None
    info_admin = None
    permisos_group = get_group_by_type(ruta)
    for permisos, group in permisos_group:
        info = calcular_info_por_agrupacion(group['emails_phishing'])
        if permisos == 0:
            tipo_usuario = 'Usuario'
            info_user = {k: v for (k, v) in zip(keys, info)}
        elif permisos == 1:
            tipo_usuario = 'Administrador'
            info_admin = {k: v for (k, v) in zip(keys, info)}
        #print(f"\nAgrupacion: {tipo_usuario}")
        #print("Numero de observaciones:", info[0])
        #print("Numero de valores ausentes (missing):", info[1])
        #print("Mediana:", info[2])
        #print("Media:", info[3])
        #print("Varianza:", info[4])
        #print("Valor máximo:", info[5])
        #print("Valor mínimo:", info[6])

    info_debil = None
    info_fuerte = None
    pwd_debil_group = get_group_by_pwd_strength(ruta)
    for passwd_debil, group in pwd_debil_group:
        info = calcular_info_por_agrupacion(group['emails_phishing'])
        if passwd_debil:
            tipo_passwd = 'Débil'
            info_debil = {k: v for (k, v) in zip(keys, info)}
        else:
            tipo_passwd = 'Fuerte'
            info_fuerte = {k: v for (k, v) in zip(keys, info)}
        #print(f"\nTipo de contraseña: {tipo_passwd}")
        #print("Numero de observaciones:", info[0])
        #print("Numero de valores ausentes (missing):", info[1])
        #print("Mediana:", info[2])
        #print("Media:", info[3])
        #print("Varianza:", info[4])
        #print("Valor máximo:", info[5])
        #print("Valor mínimo:", info[6])
    return info_user, info_admin, info_debil, info_fuerte


