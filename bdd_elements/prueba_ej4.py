import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # Declaración de las queries
    query_usuarios_criticos = '''
        SELECT nombre, emails_clicados * 1.0 / emails_phishing AS probabilidad_spam
        FROM usuarios
        WHERE pwd_debil = 1
        ORDER BY probabilidad_spam DESC
        LIMIT 10
    '''

    query_politicas_desactualizadas = '''
        SELECT nombre, cookies, aviso, proteccion_de_datos
        FROM legal
        GROUP BY nombre
        ORDER BY cookies + aviso + proteccion_de_datos DESC
        LIMIT 5
    '''


    # Conexión a la BD y creación de DFs
    con = sqlite3.connect("gicib_SI_practica1_sistemaETL.db")
    df_usuarios_criticos = pd.read_sql_query(query_usuarios_criticos, con)
    df_politicas_desactualizadas = pd.read_sql_query(query_politicas_desactualizadas, con)
    con.close()

    # Generación de los gráficos
    plt.figure(figsize=(10, 6))
    plt.bar(df_usuarios_criticos['nombre'], df_usuarios_criticos['probabilidad_spam'])
    plt.xlabel('Usuario')
    plt.ylabel('Probabilidad de pulsar en un correo de spam')
    plt.title('Usuarios más críticos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    df_politicas_desactualizadas.set_index('nombre').plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.xlabel('Página web')
    plt.ylabel('Cantidad de políticas desactualizadas')
    plt.title('Páginas web con más políticas desactualizadas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



