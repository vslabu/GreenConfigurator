from flask import Flask, request, jsonify
from waitress import serve
from flask_cors import CORS
import sys

sys.path.append('backend')

from config import jsonToConfig, Config
import chooseModel

app = Flask(__name__)
models = chooseModel.ChooseModel()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/api/getAllModelnames', methods=['GET'])
# gibt angefordertes Feature-Modell als json zurück
def getAllModelnames():
    return jsonify(models=models.getAllModels())


@app.route('/api/getFeatures', methods=['GET', 'Post'])
# gibt angefordertes Feature-Modell als json zurück
def getFeatures():
    # Variert noch wegen der verschieden Versionen, ob Modelname mitkommt oder nicht
    json_file = request.get_json()
    if json_file == None:
        return models.getFeatures()
    else:
        modelname = json_file.get("model_name")
        return models.getFeatures(modelname)

@app.route('/api/checkAndCalculate', methods=['Post'])
# prüft eine übergebene Konfiguration auf Validität
# Wenn die Konfiguration valide ist, wird diese auch sofort mit berechnet
def checkAndCalculate():
    # configs auslesen und bearbeitet
    anfrage = request.get_json()

    try:
        orig = anfrage.get("config")
        modelname = anfrage.get("model_name")
        config = jsonToConfig(orig, len(models.getModel(modelname)[1].feature.names))
        return jsonify(features=models.checkAndCalculate(config, orig, modelname))
    except:
        # TODO: ist das gutes error-handling? sollten wir ein "default-modell" haben??
        # orig = anfrage
        # config = jsonToConfig(orig, 0)
        print("konnte nicht checken")
        # return jsonify(features=models.checkAndCalculate(config, orig))


@app.route('/api/optimizeNFP', methods=['Post'])
# Optmiert eine Konfiguration nach einem bestimmten NFP, flexibel angepasst
# nach dem Grad wieviele Features geändert werden dürfen
def optimizeNFP():
    return models.generalOpt(request)

@app.route('/api/loadConfiguration', methods=['Post'])
def loadConfiguration():
    json_file = request.get_json()
    modelname = json_file.get("model_name")
    code = json_file.get("code")

    c = Config(code=code)

    return jsonify(features=models.checkAndCalculate(c, c.toJson(models.getModel(modelname)[1]), modelname))



@app.route('/api/optimizeAll', methods=['Post'])
def optimizeAll():
    # ruft optimieren auf, aber sortiert nach allen NFPs
    return models.generalOpt(request, key=lambda e: e[2])


@app.route('/api/initFeatures', methods=['Get', 'Post'])
# dient zur Initalisierung des Frontends
def initFeatures():
    # Variert noch wegen der verschieden Versionen, ob Modelname mitkommt oder nicht
    json_file = request.get_json()
    if json_file == None:
        return models.initFeatures()
    else:
        modelname = json_file.get("model_name")
        return models.initFeatures(modelname)

@app.route('/api/getSingleStats', methods=['Post'])
# prüft eine übergebene Konfiguration auf Validität
# Wenn die Konfiguration valide ist, wird diese auch sofort mit berechnet
def getSingleStats():
    # configs auslesen und bearbeitet
    anfrage = request.get_json()

    try:
        orig = anfrage.get("config")
        modelname = anfrage.get("model_name")
        config = jsonToConfig(orig, len(models.getModel(modelname)[1].feature.names))
        return jsonify(features=models.singleStats(config, orig, modelname))
    except:
        # TODO: ist das gutes error-handling? sollten wir ein "default-modell" haben??
        # orig = anfrage
        # config = jsonToConfig(orig, 0)
        print("konnte nicht checken")
        # return jsonify(features=models.checkAndCalculate(config, orig))


if __name__ == "__main__":
    app.run('127.0.0.1', port=1910, debug=True)
    serve(app)