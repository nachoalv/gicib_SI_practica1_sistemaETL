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

