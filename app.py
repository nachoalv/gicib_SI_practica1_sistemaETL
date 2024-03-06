
from flask import Flask, render_template
from bdd_elements.analisis_bd import mediaCambios2
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib
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
    return render_template('criticos.html')


@app.route('/politicas')
def politicas():
    return render_template('politicas.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
