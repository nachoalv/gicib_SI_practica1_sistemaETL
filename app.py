import json
from flask import Flask, render_template

from utils.ej2 import init as get_results
from utils.ej3 import init as get_info_by_group
from utils.ej4 import ej4ap1, ej4ap2, ej4ap3, ej4ap4

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/2')
def ej2():
    resultados = get_results("./bdd_elements")

    return render_template('ej2.html', resultados=resultados)


@app.route('/3')
def ej3():
    info_user, info_admin, info_debil, info_fuerte = get_info_by_group("./bdd_elements")

    return render_template('ej3.html',
                           info_user=info_user, info_admin=info_admin,
                           info_debil=info_debil, info_fuerte=info_fuerte)


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
