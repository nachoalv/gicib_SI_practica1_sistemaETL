import json

from flask import Flask, render_template
import matplotlib

from bdd_elements.analisis_bd import init as get_resultados
from bdd_elements.agrupaciones import init as get_info_by_group
from bdd_elements.prueba_ej4 import ej4ap1, ej4ap2, ej4ap3, ej4ap4

matplotlib.use('Agg')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


#@app.route('/MediaDeTiempo')
#def media_de_tiempo():
#    medias = ej4ap1("./bdd_elements")
#    medias_json = json.dumps(medias)
#    return render_template('media_de_tiempo.html', medias=medias_json)
#
#
#@app.route('/criticos')
#def criticos():
#    criticos = ej4ap2("./bdd_elements")
#    return render_template('criticos.html', criticos=criticos.to_dict(orient='records'))
#
#
#@app.route('/politicas')
#def politicas():
#    politicas_desactualizadas = ej4ap3("./bdd_elements")
#    cumplen_politicas = ej4ap4("./bdd_elements")
#    return render_template('politicas.html',
#                           politicas=politicas_desactualizadas.to_dict(orient='records'),
#                           cumplen_politicas=cumplen_politicas.to_dict(orient='records'))

@app.route('/2')
def ej2():
    resultados = get_resultados("./bdd_elements")
    return render_template('ej2.html', resultados=resultados)

@app.route('/3')
def ej3():
    info_user, info_admin, info_debil, info_fuerte = get_info_by_group("./bdd_elements")
    return render_template('ej3.html', info_user=info_user, info_admin=info_admin, info_debil=info_debil, info_fuerte=info_fuerte)

@app.route('/4')
def ej4():
    medias = ej4ap1("./bdd_elements")
    medias_json = json.dumps(medias)
    criticos = ej4ap2("./bdd_elements")
    politicas_desactualizadas = ej4ap3("./bdd_elements")
    cumplen_politicas = ej4ap4("./bdd_elements")

    return render_template('ej4.html',
                           medias=medias_json,
                           criticos=criticos.to_dict(orient='records'),
                           politicas=politicas_desactualizadas.to_dict(orient='records'),
                           cumplen_politicas=cumplen_politicas.to_dict(orient='records')
                           )
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
