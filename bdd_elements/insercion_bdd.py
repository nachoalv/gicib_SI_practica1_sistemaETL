import json
import sqlite3

if __name__ == '__main__':

    con = sqlite3.connect("gicib_SI_practica1_sistemaETL.db")
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS legal ''')
    cur.execute('''CREATE TABLE legal ( nombre      TEXT,
                                        cookies	    INTEGER NOT NULL CHECK(cookies in (0,1)),
                                        aviso       INTEGER NOT NULL CHECK(aviso in (0,1)),
                                        proteccion_de_datos	INTEGER NOT NULL CHECK(proteccion_de_datos in (0,1)),
                                        creacion	INTEGER NOT NULL,
                                        PRIMARY KEY(nombre))''')

    cur.execute('''DROP TABLE IF EXISTS usuarios''')
    cur.execute('''CREATE TABLE usuarios (  nombre      TEXT,
                                            telefono    INTEGER,
                                            contrasena  TEXT NOT NULL,
                                            provincia	TEXT,
                                            permisos	INTEGER NOT NULL CHECK(permisos in (0,1)),
                                            emails_total INTEGER NOT NULL,
                                            emails_phishing INTEGER NOT NULL,
                                            emails_clicados INTEGER NOT NULL,
                                            PRIMARY KEY(nombre))''')


    cur.execute('''DROP TABLE IF EXISTS cambio_psw''')
    cur.execute('''CREATE TABLE "cambio_psw" ( "id"        INTEGER,
                                            "fecha"     TEXT NOT NULL,
                                            "ip"        TEXT,
                                            "usuario"   TEXT NOT NULL,
                                            FOREIGN KEY("usuario") REFERENCES "usuarios"("nombre") ON UPDATE CASCADE ON DELETE CASCADE,
                                            PRIMARY KEY("id" AUTOINCREMENT))''')

    f = open('../data/legal_data_online.json', 'r')
    legal_data = json.load(f)
    for item in legal_data["legal"]:
        key = list(item.keys())[0]
        web = item[key]
        cur.execute('''INSERT INTO legal (nombre, cookies, aviso, proteccion_de_datos, creacion) VALUES (?, ?, ?, ?, ?)''',
                    (key, web['cookies'], web['aviso'], web['proteccion_de_datos'], web['creacion']))


    f = open('../data/users_data_online.json', 'r')
    users_data = json.load(f)
    for item in users_data["usuarios"]:
        key = list(item.keys())[0]
        user = item[key]
        if user['telefono'] == 'None':
            tlf = None
        else:
            tlf = user['telefono']
        if user['provincia'] == 'None':
            prv = None
        else:
            prv = user['provincia']
        cur.execute(
            '''INSERT INTO usuarios (nombre, telefono, contrasena, provincia, permisos, emails_total, emails_phishing, emails_clicados) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (key, tlf, user['contrasena'], prv, user['permisos'], user['emails']['total'],
             user['emails']['phishing'], user['emails']['cliclados']))
        for i in range(len(user['fechas'])):
            if user['ips'] == 'None':
                ips = None
            else:
                ips = user['ips'][i]

            fecha = user['fechas'][i] if 'fechas' in user and i < len(user['fechas']) else None
            ip = user['ips'][i] if 'ips' in user and i < len(user['ips']) else None

            cur.execute('''INSERT INTO cambio_psw (fecha, ip, usuario) VALUES (?, ?, ?)''',
                        (user['fechas'][i], ips, key))

    con.commit()
    con.close()
