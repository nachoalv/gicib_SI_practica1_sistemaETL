
from flask import Flask, render_template
from bdd_elements.analisis_bd import mediaCambios2
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib

from bdd_elements.prueba_ej4 import ej4ap3, ej4ap2, ej4ap4

matplotlib.use('Agg')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/MediaDeTiempo')
def media_de_tiempo():
    medias = mediaCambios2("./bdd_elements")
    mediaUsuario = medias[0]
    mediaAdmin = medias[1]

    labels = ['Usuario', 'Administrador']
    plt.bar(labels, medias)
    plt.xlabel('Tipo de Usuario')
    plt.ylabel('Media de Diferencia de Días')
    plt.title('Medias de Diferencia de Días por Tipo de Usuario')

    img_filename = "media_plot_ej4_1.png"

    img_path = f"static/img/{img_filename}"
    plt.savefig(img_path)
    plt.close()

    return render_template('media_de_tiempo.html', mediaUsuario=mediaUsuario, mediaAdmin=mediaAdmin, img_filename=img_filename)


@app.route('/criticos')
def criticos():
    criticos = ej4ap2("./bdd_elements")
    return render_template('criticos.html', criticos=criticos.to_dict(orient='records'))


@app.route('/politicas')
def politicas():
    politicas_desactualizadas = ej4ap3("./bdd_elements")
    cumplen_politicas = ej4ap4("./bdd_elements")
    return render_template('politicas.html',
                           politicas=politicas_desactualizadas.to_dict(orient='records'),
                           cumplen_politicas=cumplen_politicas.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
