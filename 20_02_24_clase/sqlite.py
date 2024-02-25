# W/ code with me
import json
import sqlite3

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
                                        telefono    INTEGER NOT NULL,
                                        contrasena  TEXT NOT NULL,
                                        provincia	TEXT NOT NULL,
                                        permisos	INTEGER NOT NULL CHECK(permisos in (0,1)),
                                        emails_total INTEGER,
                                        emails_phishing INTEGER,
                                        emails_clicados INTEGER,
                                        PRIMARY KEY(nombre))''')

cur.execute('''DROP TABLE IF EXISTS fechas''')
cur.execute('''CREATE TABLE "fechas" (  "fecha"     TEXT,
                                        "usuario"   TEXT,
	                                    FOREIGN KEY("usuario") REFERENCES "usuarios"("nombre") ON UPDATE CASCADE ON DELETE CASCADE,
	                                    PRIMARY KEY("fecha", "usuario"))''')

cur.execute('''DROP TABLE IF EXISTS ips''')
cur.execute('''CREATE TABLE "ips" ( "ip"     TEXT,
                                    "usuario"   TEXT,
	                                FOREIGN KEY("usuario") REFERENCES "usuarios"("nombre") ON UPDATE CASCADE ON DELETE CASCADE,
	                                PRIMARY KEY("ip", "usuario"))''')

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
    cur.execute(
        '''INSERT INTO usuarios (nombre, telefono, contrasena, provincia, permisos, emails_total, emails_phishing, emails_clicados) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (key, user['telefono'], user['contrasena'], user['provincia'], user['permisos'], user['emails']['total'],
         user['emails']['phishing'], user['emails']['cliclados']))
    for fecha in user['fechas']:
        try:
            cur.execute('''INSERT INTO fechas (fecha, usuario) VALUES (?, ?)''',
                        (fecha, key))
        except sqlite3.IntegrityError:
            print("repetido: "+key+" "+fecha)
    for ip in user['ips']:
        try:
            cur.execute('''INSERT INTO ips (ip, usuario) VALUES (?, ?)''',
                        (ip, key))
        except sqlite3.IntegrityError:
            print("repetido: "+key+" "+ip)

con.commit()
con.close()
