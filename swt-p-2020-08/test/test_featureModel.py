# kompletter Test muss noch geprüft werden, ob dies ausreichend ist
import featureModel
import os
import xmltodict
import json
import pytest


def test_StandardFileEinlesen():
    ergebnis = True
    try:
        test1 = featureModel.FeatureModel()
        test2 = featureModel.FeatureModel(feat="FeatureModel")
        test3 = featureModel.FeatureModel("FeatureModel")
    except:
        ergebnis = False
    assert ergebnis


def test_FalscheDateiEinlesen():
    ergebnis = True
    try:
        test2 = featureModel.FeatureModel("fehler")
    except:
        ergebnis = False
    assert not ergebnis


def test_Datentest():
    test7 = featureModel.FeatureModel()
    ergebnis = True
    name = []
    rules = []
    xml_in_json = ''
    try:
        file = open(os.path.dirname(__file__) + '/../app/data/HSQL DB/FeatureModel.dimacs', "r")
        for x in file:
            # Zeile zerlegen
            line = x.split(" ")

            # Aufteilen der Zeilen nach Namen und Regeln
            if line[0] == 'c':
                name.append([line[1], line[2].replace("\n", "")])
            elif line[0] == 'p':
                pass
            else:
                line_int = []
                line[len(line) - 1] = line[len(line) - 1].replace("\n", "")
                i = 0
                while i < len(line) - 1:
                    line_int.append(int(line[i]))
                    i = i + 1
                rules.append(line_int)

    except:
        raise Exception("File nicht vorhanden")
        ergebnis = False

    assert ergebnis
    assert name == test7.names
    assert rules == test7.rules

    try:
        # XML-File öffnen und einlesen und umwandeln in json-Datei
        with open(os.path.dirname(__file__) + '/../app/data/HSQL DB/FeatureModel.xml', "r") as xmlFile:
            obj = xmltodict.parse(xmlFile.read())
        xml_in_json = json.dumps(obj)

    except FileNotFoundError:
        raise Exception("File nicht vorhanden")
        ergebnis = False

    assert ergebnis
    assert xml_in_json == test7.xmlInJSon