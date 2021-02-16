import performanceInfluenceModel
import featureModel
from config import Config
import pytest


feature = featureModel.FeatureModel()


def test_StandardFileEinlesen():
    ergebnis = True
    try:
        test1 = performanceInfluenceModel.PerformanceInfluenceModel(feature)
        test1 = performanceInfluenceModel.PerformanceInfluenceModel(feature, "model")
        test1 = performanceInfluenceModel.PerformanceInfluenceModel(feature, perf="model")
    except:
        ergebnis = False
    assert ergebnis


def test_FalscheDateiEinlesen():
    ergebnis = True
    try:
        test2 = performanceInfluenceModel.PerformanceInfluenceModel(feature, "Fehler")
    except:
        ergebnis = False
    assert not ergebnis


def test_MethodenAufAusfuehrbarkeit():
    ergebnis = True
    test3 = performanceInfluenceModel.PerformanceInfluenceModel(feature)
    try:
        stats = test3.getStats(Config(options=[1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]))
    except:
        ergebnis = False
    assert ergebnis
