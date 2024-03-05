from flask import Flask, render_template

from bdd_elements.analisis_bd import mediaCambios

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/MediaDeTiempo')
def media_de_tiempo():

    return render_template('media_de_tiempo.html', media=mediaCambios())

@app.route('/criticos')
def criticos():
    return render_template('criticos.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
