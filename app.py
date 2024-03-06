from flask import Flask, render_template

from bdd_elements.analisis_bd import mediaCambios2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/MediaDeTiempo')
def media_de_tiempo():
    medias, img_filename = mediaCambios2("./bdd_elements")
    mediaUsuario = medias[0]
    mediaAdmin = medias[1]
    return render_template('media_de_tiempo.html', mediaUsuario=mediaUsuario, mediaAdmin=mediaAdmin, img_filename=img_filename)


@app.route('/criticos')
def criticos():
    return render_template('criticos.html')


@app.route('/politicas')
def politicas():
    return render_template('politicas.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
