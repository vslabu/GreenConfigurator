from flask import jsonify

import model
import os

from config import jsonToConfig


# Klasse ChooseModel
# Methoden :    Konstruktor
#               getAllModels
#               getFeatures
#               getModel
#               checkAndCalculate
#               generalOpt
#               initFeatures

# Dient zur Auswahl und Speicherung der verschiedenen Modelle, so dass die Anfrage an das richtige Modell weitergeleitet wird
class ChooseModel:

    # Konstruktur liest alle verfügbaren Modelle ein
    def __init__(self):

        # speichert den Modell Namen und das dazugehörige Modell
        self.models = []

        # Ordnerweise die Modelle einlesen
        pfad = (os.path.dirname(__file__) + '/../data/')
        for foldername in next(os.walk(os.path.dirname(__file__) + '/../data/'))[1]:

            # Namen der Dateien und des Ordners zum Einlesen bestimmen mittles Parsen
            modelname = foldername
            feat = ""
            perf = ""
            xml = ""
            # Auswertung des Files, welche zum Einlesen des Modells benötigt werden
            for file in os.listdir(os.path.dirname(__file__) + '/../data/' + foldername):
                datei = file.split(".")
                if datei[1] == 'dimacs':
                    feat = datei[0]
                elif datei[1] == 'csv':
                    perf = datei[0]
                elif datei[1] == 'xml':
                    xml = datei[0]

            # Model generieren und in die ModelListe einfügen
            mod = model.Model(feat=feat, perf=perf, xml=xml, foldername=foldername)
            self.models.append((foldername, mod))

    # liefter alle verfügbaren Modelle an das Frontend, welche zur Verfügung stehen
    def getAllModels(self):
        # Auslesen der Modelnamen
        namensliste = []
        for name in self.models:
            namensliste.append(name[0])
        return namensliste

    # sucht das passende Modell zum Modelnamen und gibt die JSON zurück
    # TODO Abfangen bei falschem Modellnamen
    def getFeatures(self, modelname="HSQL DB"):
        for mod in self.models:
            if modelname == mod[0]:
                return mod[1].feature.xmlInJSon

    # liefert das Model ausgewählte Model
    def getModel(self, modelname):
        for mod in self.models:
            if modelname == mod[0]:
                return mod

    # checkAndCalculate an das richtige Modell weiterleiten
    def checkAndCalculate(self, con, orig, modelname="HSQL DB"):
        # wählt das entsprechende Modell zur Berechnung aus
        for mod in self.models:
            if modelname == mod[0]:

                # Prüfen und Berechnen der Konfiguration
                # check: Ist Konfiguration valide?
                # con: Unveränderte Konfiguration
                # stats: Werte für die NFPs
                (check, con, stats) = mod[1].checkAndCalculate(con)
                # rückgabe der NFP
                nfp = {}
                for i in range(0, mod[1].performance.nfpNumber):
                    nfp.update({mod[1].performance.nfpNames[i]: stats[i] if check else 0})

                return {"model_name": modelname, "features": orig, "nfp": nfp, "verified": check, "code": con.getCode()}
        return {"model_name": None, "features": orig, "nfp": 0, "verified": False, "code": None}

    # leitet die allgemeine Optimierung ein
    def generalOpt(self, request, key=''):
        # configs auslesen und bearbeiten
        json_file = request.get_json()
        depth = json_file.get("depth")
        nfp = json_file.get("nfp")
        modelname = json_file.get("model_name")
        # Variert noch wegen der verschieden Versionen, ob Modelname mitkommt oder nicht
        if modelname is None:
            modelname = "HSQL DB"

        orig = json_file.get("config")

        # mit entsprechenden Modell die Optimierung für die Config vornehmen
        for mod in self.models:
            if modelname == mod[0]:

                config = jsonToConfig(orig, len(mod[1].feature.names))
                conResult = []
                # Optimierung durchführen
                try:
                    (check, con, stats) = mod[1].optimizeFor(con=config, depth=depth, nfp=nfp, key=key)
                    conResult = con.toJson(mod[1])
                except Exception as e:
                    print(e)
                    # Falls eine falsche Config übermittelt wird, wird verified als False gesetzt
                    stats = []
                    check = False

                # berechnetetes Ergebnis ins Json-Format bringen
                nfpList = {}
                for i in range(0, mod[1].performance.nfpNumber):
                    nfpList.update({mod[1].performance.nfpNames[i]: stats[i] if check else 0})

                con = con if con else config

                return jsonify(features={"model_name": modelname,
                                         "features": conResult if conResult else orig,
                                         "nfp": nfpList,
                                         "verified": check,
                                         "code": con.getCode()})

        return jsonify(features={"model_name": None, "features": orig, "nfp": nfp, "verified": False, "code": None})

    # liefert dem Frontend alle nötigen Informationen zur Initalisierung des Frontends
    def initFeatures(self, modelname="HSQL DB"):
        for mod in self.models:
            if modelname == mod[0]:
                return jsonify(model={"model_name": mod[0],
                                      "features": mod[1].feature.angepassteJson,
                                      "nfp": mod[1].nfpJson,
                                      "config": mod[1].feature.configurationList,
                                      "bestConfigs": mod[1].bestConfigs,
                                      "worstConfigs": mod[1].worstConfigs})



    # checkAndCalculate an das richtige Modell weiterleiten
    def singleStats(self, con, orig, modelname="HSQL DB"):
        # wählt das entsprechende Modell zur Berechnung aus
        for mod in self.models:
            if modelname == mod[0]:

                # Prüfen und Berechnen der Konfiguration
                # check: Ist Konfiguration valide?
                # con: Unveränderte Konfiguration
                # stats: Werte für die NFPs
                (check, con, singlefeats) = mod[1].singleStats(con)

                convertSinFeat = []
                # einzeln berechneten Features an das richtige Format anpassen
                for i in singlefeats:
                    nfp = {}
                    for j in range(0, mod[1].performance.nfpNumber):
                        nfp.update({mod[1].performance.nfpNames[j]: i[1][j]})
                    convertSinFeat.append({"id": i[0], "name": i[2], "nfp": nfp})


                return {"model_name": modelname, "features": orig, "singlefeats": convertSinFeat}
        return {"model_name": None, "features": orig, "singlefeat": None}
