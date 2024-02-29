import sqlite3
import pandas as pd
import hashlib


def cargar_wordlist(diccionario):
    with open(diccionario, 'r', encoding='latin-1') as f:
        return [line.strip() for line in f]


def hash_md5(passwd):
    return hashlib.md5(passwd.encode()).hexdigest()


def es_passwd_debil(hash_passwd, passwds_debiles):
    return hash_passwd in passwds_debiles


def calcular_info_por_agrupacion(data):
    num_observaciones = data.count()
    num_valores_ausentes = data.isnull().sum()
    mediana = data.median()
    media = data.mean()
    varianza = data.var()
    maximo = data.max()
    minimo = data.min()
    return num_observaciones, num_valores_ausentes, mediana, media, varianza, maximo, minimo


if __name__ == '__main__':
    con = sqlite3.connect("gicib_SI_practica1_sistemaETL.db")
    passwds_debiles = set(hash_md5(passwd) for passwd in cargar_wordlist('../data/SmallRockYou.txt'))

    query = '''
        SELECT permisos, emails_phishing, contrasena
        FROM usuarios
        WHERE emails_phishing IS NOT NULL
    '''

    df = pd.read_sql_query(query, con)
    con.close()

    print('='*30+'Agrupaciones SEPARADAS'+'='*30)
    for permisos, group in df.groupby('permisos'):
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


    for passwd_debil, group in df.groupby(
            df.apply(lambda row: es_passwd_debil(row['contrasena'], passwds_debiles), axis=1)):
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

    print('='*30+'Agrupaciones COMBINADAS'+'='*30)
    for permisos, group in df.groupby('permisos'):
        if permisos == 0:
            tipo_usuario = 'Usuario'
        elif permisos == 1:
            tipo_usuario = 'Administrador'
        print(f"\nAgrupacion: {tipo_usuario}")
        for passwd_debil, group_c in group.groupby(
                df.apply(lambda row: es_passwd_debil(row['contrasena'], passwds_debiles), axis=1)):
            if passwd_debil:
                tipo_passwd = 'Débil'
            else:
                tipo_passwd = 'Fuerte'
            print(f"\nTipo de contraseña: {tipo_passwd}")
            info = calcular_info_por_agrupacion(group_c['emails_phishing'])
            print("Numero de observaciones:", info[0])
            print("Numero de valores ausentes (missing):", info[1])
            print("Mediana:", info[2])
            print("Media:", info[3])
            print("Varianza:", info[4])
            print("Valor máximo:", info[5])
            print("Valor mínimo:", info[6])
