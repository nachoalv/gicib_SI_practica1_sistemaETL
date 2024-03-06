import sqlite3

import pandas as pd

def init():
    con = sqlite3.connect("gicib_SI_practica1_sistemaETL.db")

    query_num_muestras = '''
        SELECT COUNT(*) 
        FROM usuarios 
        WHERE telefono IS NOT NULL AND provincia IS NOT NULL
        '''

    query_fechas = '''
        SELECT COUNT(DISTINCT fecha) AS num_fechas
        FROM cambio_psw 
        WHERE usuario IN (SELECT nombre FROM usuarios WHERE telefono IS NOT NULL AND provincia IS NOT NULL) 
        GROUP BY usuario
    '''

    query_ips = '''
        SELECT COUNT(DISTINCT ip) AS num_ips 
        FROM cambio_psw 
        WHERE usuario IN (SELECT nombre FROM usuarios WHERE telefono IS NOT NULL AND provincia IS NOT NULL) 
        GROUP BY usuario
    '''

    query_emails_phishing = '''
        SELECT emails_clicados 
        FROM usuarios 
        WHERE telefono IS NOT NULL AND provincia IS NOT NULL
    '''

    query_emails_total = '''
        SELECT emails_total
        FROM usuarios 
        WHERE telefono IS NOT NULL AND provincia IS NOT NULL
    '''

    query_emails_phishing_admin = '''
        SELECT emails_clicados 
        FROM usuarios 
        WHERE permisos = 1 AND telefono IS NOT NULL AND provincia IS NOT NULL
    '''

    num_muestras = pd.read_sql_query(query_num_muestras, con).iloc[0, 0]

    fechas_cambio_psw = pd.read_sql_query(query_fechas, con)
    ips_detectadas = pd.read_sql_query(query_ips, con)
    emails_phishing = pd.read_sql_query(query_emails_phishing, con)
    emails_phishing_admin = pd.read_sql_query(query_emails_phishing_admin, con)
    emails_total = pd.read_sql_query(query_emails_total, con)
    con.close()

    media_fechas = fechas_cambio_psw.mean().values[0]
    media_ips = ips_detectadas.mean().values[0]
    media_emails_phishing = emails_phishing.mean().values[0]

    desviacion_fechas = fechas_cambio_psw.std().values[0]
    desviacion_ips = ips_detectadas.std().values[0]
    desviacion_emails_phishing = emails_phishing.std().values[0]

    min_emails_total = emails_total.min().values[0]
    max_emails_total = emails_total.max().values[0]
    min_emails_admin = emails_phishing_admin.min().values[0]
    max_emails_admin = emails_phishing_admin.max().values[0]

    print("Número de muestras:", num_muestras)
    print("Media del total de fechas en las que se ha cambiado la contraseña:", media_fechas)
    print("Desviación estándar del total de fechas en las que se ha cambiado la contraseña:", desviacion_fechas)
    print("Media del total de IPs que se han detectado:", media_ips)
    print("Desviación estándar del total de IPs que se han detectado:", desviacion_ips)
    print("Media del número de email interactuados de phishing:", media_emails_phishing)
    print("Desviación estándar del número de email interactuados de phishing:", desviacion_emails_phishing)
    print("Valor mínimo del total de emails recibidos:", min_emails_total)
    print("Valor máximo del total de emails recibidos:", max_emails_total)
    print("Valor mínimo del total de emails de phishing interactuados por admins:", min_emails_admin)
    print("Valor máximo del total de emails de phishing interactuados por admins:", max_emails_admin)

def mediaCambios(ruta):
    con = sqlite3.connect(f"{ruta}/gicib_SI_practica1_sistemaETL.db")
    query_fechas = '''
        SELECT fechas
        FROM cambio_psw 
        WHERE usuario IN (SELECT nombre FROM usuarios WHERE telefono IS NOT NULL AND provincia IS NOT NULL) 
    '''
    print(query_fechas)
    fechas_cambio_psw = pd.read_sql_query(query_fechas, con)
    media_fechas = fechas_cambio_psw.mean().values[0]
    return media_fechas


def mediaCambios2(ruta):
    con = sqlite3.connect(f"{ruta}/gicib_SI_practica1_sistemaETL.db")
    query_fechas = '''
        SELECT usuario, fecha, permisos
        FROM cambio_psw 
        JOIN usuarios ON cambio_psw.usuario = usuarios.nombre
        WHERE usuario IN (SELECT nombre FROM usuarios WHERE telefono IS NOT NULL AND provincia IS NOT NULL) 
        '''

    usuarios_fechas_cambio_psw = pd.read_sql_query(query_fechas, con)
    usuarios_fechas_cambio_psw['fecha'] = pd.to_datetime(usuarios_fechas_cambio_psw['fecha'], format="%d/%m/%Y")

    usuarios_fechas_cambio_psw = usuarios_fechas_cambio_psw.sort_values('fecha')
    grouped_by_user = usuarios_fechas_cambio_psw.groupby('usuario')

    info_needed_arr = []

    for user, group in grouped_by_user:
        permisos = group['permisos'].iloc[0]
        anterior = None
        for index, fecha in enumerate(group['fecha']):
            if index:
                dif = fecha - anterior
                info_needed_arr.append([user, dif.days, permisos])
            anterior = fecha

    info_needed_df = pd.DataFrame(info_needed_arr, columns=['usuario', 'dif', 'permisos'])
    group_by_perm = info_needed_df.groupby('permisos')
    medias = [0, 0]
    for permisos, group in group_by_perm:
        if permisos == 0:
            # tipo_usuario = 'Usuario'
            medias[0] = group['dif'].mean()
        elif permisos == 1:
            # tipo_usuario = 'Administrador'
            medias[1] = group['dif'].mean()
        # print(f"\nAgrupacion: {tipo_usuario}")
        # print(group['dif'].mean())

    return medias


if __name__ == "__main__":
    mediaCambios2(".")
