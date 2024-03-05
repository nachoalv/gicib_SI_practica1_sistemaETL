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

def get_group_by_type():
    con = sqlite3.connect("gicib_SI_practica1_sistemaETL.db")
    query = '''
            SELECT *
            FROM usuarios
            WHERE emails_phishing IS NOT NULL
            '''
    df = pd.read_sql_query(query, con)
    con.close()
    return df.groupby('permisos')

def get_group_by_pwd_strength():
    con = sqlite3.connect("gicib_SI_practica1_sistemaETL.db")
    query = '''
            SELECT *
            FROM usuarios
            WHERE emails_phishing IS NOT NULL
            '''
    df = pd.read_sql_query(query, con)
    con.close()
    return df.groupby('pwd_debil')


if __name__ == '__main__':
    permisos_group = get_group_by_type()
    for permisos, group in permisos_group:
        if permisos == 0:
            tipo_usuario = 'Usuario'
        elif permisos == 1:
            tipo_usuario = 'Administrador'
        print(f"\nAgrupacion: {tipo_usuario}")
        info = calcular_info_por_agrupacion(group['emails_phishing'])
        print("Numero de observaciones:", info[0])
        print("Numero de valores ausentes (missing):", info[1])
        print("Mediana:", info[2])
        print("Media:", info[3])
        print("Varianza:", info[4])
        print("Valor máximo:", info[5])
        print("Valor mínimo:", info[6])


    pwd_debil_group = get_group_by_pwd_strength()
    for passwd_debil, group in pwd_debil_group:
        if passwd_debil:
            tipo_passwd = 'Débil'
        else:
            tipo_passwd = 'Fuerte'
        print(f"\nTipo de contraseña: {tipo_passwd}")
        info = calcular_info_por_agrupacion(group['emails_phishing'])
        print("Numero de observaciones:", info[0])
        print("Numero de valores ausentes (missing):", info[1])
        print("Mediana:", info[2])
        print("Media:", info[3])
        print("Varianza:", info[4])
        print("Valor máximo:", info[5])
        print("Valor mínimo:", info[6])
