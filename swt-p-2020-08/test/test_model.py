# Test bei dem die Berechnung auf Korrektheit geprüft wird, muss noch erstellt werden
# Test für optimizeFor, getSimilar
# FIXME: constant import errors when running tests
import model
import pytest
from config import Config
import csv
import itertools
from model import Model
from distutils.util import strtobool
import os

def test_KlasseGenerieren():
    ergebnis = True
    try:
        mod = model.Model()
    except:
        ergebnis = False
    assert ergebnis

    ergebnis = True
    try:
        mod = model.Model(feat="FeatureModel", perf="model")
    except:
        ergebnis = False
    assert ergebnis

def test_KlasseGenerierenFehler():
    ergebnis = True
    try:
        mod = model.Model(feat='test')
    except:
        ergebnis = False
    assert not ergebnis

    ergebnis = True
    try:
        mod = model.Model(perf='test')
    except:
        ergebnis = False
    assert not ergebnis

    ergebnis = True
    try:
        mod = model.Model(perf='test', feat="test")
    except:
        ergebnis = False
    assert not ergebnis

def test_getFeatures():
    ergebnis = True
    try:
        mod = model.Model()
    except:
        ergebnis = False
    assert ergebnis

def test_checkAndCalculate():
    ergebnis = True

    # korrekte Config
    try:
        mod = model.Model()
        (check, _, _) = mod.checkAndCalculate(Config(options=[1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]))
    except:
        check = False
    assert check

    # falsche Config
    try:
        (check, _, _) = mod.checkAndCalculate(Config(options=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0]))
    except:
        check = False
    assert not check

    # zu kurze Config
    try:
        (check, _, _) = mod.checkAndCalculate((Config(options=[1, 1, 1, 1, 1, 0, 0, 0])))
    except:
        check = False
    assert not check

    # zu lange Config
    try:
        (check, _, _) = mod.checkAndCalculate(Config(options=([1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0])))
    except:
        check = False
    assert not check


@pytest.mark.csv
def test_checkAndCalculate_csv():
    result = True

    # creates list of all possible configurations for testing
    input_configs = list(map(list, itertools.product([0, 1], repeat=18)))
    mod = Model()

    try:
        with open(os.path.dirname(__file__) + '/test_data.csv', mode='r', newline='') as f:

            # reading expected output
            reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # i: counting index starting from 0
            for i, line in enumerate(reader):

                # input configuration to test: {Check={True|False}, Config={(0,1)^18}, NFPs if valid}
                con = list(mod.checkAndCalculate(Config(options=input_configs[i])))

                # 2 variables extracted from expected output line for readability
                exp_checked = bool(strtobool(line[0]))
                exp_nfps = [float(boo) for boo in line[19:]]

                if con[0] == exp_checked:
                    if con[0] & (con[2] == exp_nfps):
                        result
                    elif (con[0] is False) & len(con[2]) == 0:
                        result
                    else:
                        result = False
                else:
                    result = False
    except Exception as e:
        print(e)
        result = False

    print("\t", i+1, " configurations totally tested.")
    assert result, "Eine Konfiguration wurde falsch berechnet"
