import copy
import os
import shelve
import sys

from config import Config
from performanceInfluenceModel import PerformanceInfluenceModel
from featureModel import FeatureModel


# Klasse Model
# Methoden :    Konstruktor
#               checkAndCalculate
#               optimizeFor
#               optimize
#               changeNumeric
#               checkStats
#               loadBorder
#               generateDataCache

# Klasse für alles zu einem Model
class Model:

    # generiert das Model zur Kommunikation mit dem Server und der eigentlichen Daten
    # @param feat übernimmt die DIMACS und die CSV-Datei und gibt diese weiter
    def __init__(self, feat="FeatureModel", perf="model", xml="FeatureModel", foldername="HSQL DB"):

        # speichert die NFP-Liste fürs Frontend mit den berechneten Grenzen für die Diagramme
        self.nfpJson = []
        # speichert die Codes der besten Configs
        self.bestConfigs = []
        # speichert die Codes der schlechtestn Configs
        self.worstConfigs = []

        # enthält das Feature Model
        self.feature = FeatureModel(feat, xml, foldername)
        # enthält das Performance Influence Model
        self.performance = PerformanceInfluenceModel(self.feature, perf, foldername)
        # lädt die Grenzen und generiert die angepasste json Datei fürs Frontend
        self.loadBorder(foldername)

    # ist der Methodenaufruf zur Prüfung einer Konfiguration
    # @param bekommt eine Config übergeben
    def checkAndCalculate(self, con):
        # prüft zuerst die Config auf Korrektheit
        # speichert Ergebnis und ruft Berechnung auf
        try:
            check = self.feature.validate(con)
        # wird ausgeführt, wenn die Configuration eine inkorrekte Länge hat
        except:
            check = False

        if check:
            return (check, con, self.performance.getStats(con))
        else:
            return (check, con, [])

    # ist der Methodenaufruf zur Prüfung einer Konfiguration
    # @param bekommt eine Config übergeben
    def singleStats(self, con):
        # prüft zuerst die Config auf Korrektheit
        # speichert Ergebnis und ruft Berechnung auf
        try:
            check = self.feature.validate(con)
        # wird ausgeführt, wenn die Configuration eine inkorrekte Länge hat
        except:
            check = False

        if check:
            return (check, con, self.performance.getSingleStats(con))
        else:
            return (check, con, [])

    # Methodenaufruf zur Optimierung
    # @con enthält die Konfiguration, die optimiert werden soll
    # @depth übernimmt den Grad wieviele Features hinzu bzw. abgewählt werden können
    # @nfp ist ein String und gibt an, welcher NFP-Wert optimiert werden soll
    # @key
    # @numopt gibt an ob numerische Optimierung erlaubt ist
    # @numStep gibt an ob nur ein Schritt bei den numerischen Werten erlaubt ist oder ob alle möglichen Schritte gehen
    # @worst wenn eine schlechtere statt eine bessere Configuration gefunden werden muss
    # @return ist dann die optimierte Config mit den berechneten NFPs
    def optimizeFor(self, con, depth=1, nfp='', key='', numOpt=True, numStep=True, worst=False):
        # prüft zuerst die vorhandene Konfiguration auf Korrektheit und berechnet die Konfiguration
        (check, con, stats) = self.checkAndCalculate(con)

        if not check:
            raise Exception("Die Konfiguration ist nicht valide")

        # Prüfen ob ein NFP angegeben ist, nach dem optimiert werden soll
        if nfp == '' and key == '':
            raise Exception("Es ist kein Wert für die Optimierung angegeben")
        elif key == '':
            # index der NFP in der Liste von NFP-Namen
            posNfp = self.performance.nfpNames.index(nfp)
        # wenn prozentual über alle NFP´s optimiert werden soll
        if nfp == None:
            posNfp = 'all'
        # Start der eigentlichen Optimierung
        (ergebnis_con, ergebnis_stats) = self.optimize(con, stats, 0, depth, posNfp, numOpt, numStep, worst)
        return (check, ergebnis_con, ergebnis_stats)

    # Optimierungsroutine
    # @con ist die eingegebene Konfiguration
    # @stats sind die berechneten NFP´s
    # @depth ist die Suchtiefe
    # @posNfp gibt Stelle an, an welcher geändert werden soll
    # @numOpt ob numerische Werte mitoptimiert werden
    # @numStep ob nur ein numerische Schritt erlaubt ist oder bis zum Ende
    # @worst gibt an ob eine schlechtere Config gesucht werden soll
    def optimize(self, con, stats, posChange, depth, posNfp, numOpt, numStep, worst):

        # der Ergebniskondiguration die eingegebene Liste zuweisen
        resultcon = con
        resultstats = stats
        # Stelle ab welcher die Konfiguration bearbeitet werden soll
        i = posChange
        # merkt sich ob in beide Richtungen der numerische Wert getestet wurde
        count_UP = False
        # um zu signalisieren, dass alle Schritte der numerischen Werte gegangen wurden
        madeAllSteps = True

        # Anzahl der möglichen änderbaren Features
        while i < len(self.feature.names + self.feature.numericNames):
            # Kopie der Inputliste erstellen, enthält aber nur die Features ohne NFP´s in diesem Moment
            # beziehnungsweise wird die Liste nach einem Durchlauf zurückgesetzt, damit das nächste Feature
            # geändert wird
            if madeAllSteps:
                optCon = copy.deepcopy(con)

            # jetzt die entsprechendes Feature an der Postion umschalten
            # wenn es kleiner ist als die Länge der Featurenamen, dann ist es ein Boolescher Wert
            # ansonsten eine numerischer Wert
            if i < len(self.feature.names):
                if optCon.options[i]:
                    optCon.options[i] = 0
                else:
                    optCon.options[i] = 1
            else:
                # Änderung des numerischen Wertes
                # muss in Ruhe getestet werden, aber mit momentanen Configaufbau nicht möglich
                # Position den numerischen Feature in Liste finden
                # Vorraussetzung numerische Optimierung ist gewünscht
                if numOpt:
                    j = 0
                    while j < len(self.feature.numericNames):
                        if str(i + 1) in self.feature.numericNames[j]:
                            posNumFeat = j
                            break
                        j = j + 1

                    numericField = self.feature.numericNames[posNumFeat]

                    # prüfen ob nur ein Step oder alle Steps erlaubt sind
                    if numStep:
                        # für nur einen Schritt
                        if not count_UP:
                            # erst Wert verringern
                            optCon = self.changeNumeric(optCon, posNumFeat, numericField, count_UP)
                            # um im nächsten Schritt zu erhöhen
                            count_UP = True
                        else:
                            # Gegenrichtung prüfen, Wert erhöhen
                            optCon = self.changeNumeric(optCon, posNumFeat, numericField, count_UP)
                            # um beim nächsten Mal zu verringern
                            count_UP = False

                    else:
                        # wenn alle möglichen Schritte gegangen werden sollen
                        madeAllSteps = False
                        if not count_UP:
                            # Wenn der aktuelle Wert größer als die Mindestgrenze ist,
                            # kann dieser verändert werden
                            # danach Operator auswerten (+ oder Mal)

                            if optCon.numeric[posNumFeat] > numericField[2]:
                                optCon = self.changeNumeric(optCon, posNumFeat, numericField, count_UP)
                            else:
                                count_UP = True
                                # um Config wieder zurückzusetzen, damit in die Gegenrichtung gegangen werden kann
                                optCon = copy.deepcopy(con)
                        else:
                            if optCon.numeric[posNumFeat] < numericField[3]:
                                optCon = self.changeNumeric(optCon, posNumFeat, numericField, count_UP)
                            else:
                                count_UP = False
                                madeAllSteps = True

            # geänderte Config prüfen
            (check, optCon, optConStats) = self.checkAndCalculate(optCon)

            # ergebnis auswerten
            # bei False, ist die Config invalide, muss also nicht weiter betrachtet werden
            # bei true valide Config und prüfen ob besser, wenn ja Referenz speichern in result_config
            if check:
                # Vergleich des aktuellen Ergebnis mit dem aktuellen von result_config
                # wenn neues Ergebnis kleiner ist, dann übernehme die neue Konfiguration
                (resultcon, resultstats) = self.checkStats(resultcon, resultstats, optCon, optConStats, posNfp, worst)

            # Falls der grade größer 1 ist, so kann eine weitere Variable bearbeitet werden
            # somit ein rekursiver Aufruf der die Stelle dahinter verändert, um alle Varianten zu testen
            if depth > 1:
                pos_change = i
                (returncon, returnstats) = self.optimize(optCon, resultstats, pos_change + 1, depth - 1, posNfp, numOpt,
                                                         numStep, worst)
                # rueckgabe prüfen, ob es die gleiche ist, wenn ja, dann ignorieren,
                # sonst prüfen, ob NFP besser, wenn ja übernehmen
                if returncon != optCon:
                    (resultcon, resultstats) = self.checkStats(resultcon, resultstats, returncon, returnstats, posNfp,
                                                               worst)

            # Bedingungen wann zum nächsten Feature übergegangen werden kann
            if not count_UP and madeAllSteps:
                i = i + 1

        # Rückgabe der gefundenen Konfiguration
        return (resultcon, resultstats)

    # ändert einen numerischen Wert ab
    # @optCon ist die zu ändernde Konfiguration
    # @posNumFeat gibt die Position vom Feature das geändert wird
    # @numericField gibt das Feld mit allen notwendigen Daten über das numerische Feature
    # @count_UP gibt an ob hoch oder runtergezählt wird
    @staticmethod
    def changeNumeric(optCon, posNumFeat, numericField, count_UP):
        if not count_UP:
            # Wenn der aktuelle Wert größer als die Mindestgrenze ist,
            # kann dieser verändert werden
            # danach Operator auswerten (+ oder Mal)
            if optCon.numeric[posNumFeat] > numericField[2]:
                if numericField[5] == '+':
                    optCon.numeric[posNumFeat] = optCon.numeric[posNumFeat] - numericField[4]
                else:
                    optCon.numeric[posNumFeat] = optCon.numeric[posNumFeat] / numericField[4]
        else:
            # Gegenrichtung
            # Prüfen ob kleiner Maximalwert
            if optCon.numeric[posNumFeat] < numericField[3]:
                if numericField[5] == '+':
                    optCon.numeric[posNumFeat] = optCon.numeric[posNumFeat] + numericField[4]
                else:
                    optCon.numeric[posNumFeat] = optCon.numeric[posNumFeat] * numericField[4]

        return optCon

    # prüft ob Konfiguration besser geworden ist
    @staticmethod
    def checkStats(resultcon, resultstats, optCon, optConStats, posNfp, worst):

        # Entscheidung ob alle oder ein spezielles Feature geprüft wird
        if posNfp == 'all':
            pos_Nfp = 0
            nfp_procent = []
            # prozentuale Berechnung der Ergebnisse im Vergleich
            while pos_Nfp < len(optConStats):
                nfp_procent.append((optConStats[pos_Nfp] * 100 / resultstats[pos_Nfp]) - 100)
                pos_Nfp = pos_Nfp + 1
            procent_absolut = 0
            # zählt die Ergebnisse prozentual zusammen
            for j in nfp_procent:
                procent_absolut = procent_absolut + j

            # absolute Prozentwert, wenn dieser kleiner als Null ist, dann ist die Konfiguration besser
            # prüft ob es besser oder schlechter werden soll, je nach Configurationsziel
            if not worst:
                if procent_absolut < 0:
                    resultcon = optCon
                    resultstats = optConStats
            else:
                if procent_absolut > 0:
                    resultcon = optCon
                    resultstats = optConStats
        else:
            # Optimieren nach einem fest vorgegebenen Feature
            if not worst:
                # prüft ob neue Config besser ist
                if optConStats[posNfp] < resultstats[posNfp]:
                    resultcon = optCon
                    resultstats = optConStats
                # wenn das Feature gleich ist, werden die anderen betrachtet
                elif optConStats[posNfp] == resultstats[posNfp]:
                    pos_nfp = 0
                    optimiert = False
                    while pos_nfp < len(optConStats) and not optimiert:
                        if optConStats[pos_nfp] < resultstats[pos_nfp]:
                            resultcon = optCon
                            resultstats = optConStats
                            optimiert = True
                        pos_nfp = pos_nfp + 1
            else:
                # das gleiche wie dadrüber, nur in die Gegenrichtung
                if optConStats[posNfp] > resultstats[posNfp]:
                    resultcon = optCon
                    resultstats = optConStats
                elif optConStats[posNfp] == resultstats[posNfp]:
                    pos_nfp = 0
                    optimiert = False
                    while pos_nfp < len(optConStats) and not optimiert:
                        if optConStats[pos_nfp] > resultstats[pos_nfp]:
                            resultcon = optCon
                            resultstats = optConStats
                            optimiert = True
                        pos_nfp = pos_nfp + 1

        return resultcon, resultstats

    # dient zum generieren der Grenzen
    def loadBorder(self, folder="HSQL DB"):
        # Prüfen ob Cache-File vorhanden ist
        # wenn ja einlesen, ansonsten anlegen
        if os.path.exists(os.path.dirname(__file__) + '/../data/' + folder + "/data_cache.slv.dat"):
            try:
                # file öffnen und Listen auslesen
                file = shelve.open(os.path.dirname(__file__) + '/../data/' + folder + "/data_cache.slv")
            except FileNotFoundError:
                raise Exception("File not found")

            if "nfpJson" in file:
                self.nfpJson = file["nfpJson"]
                self.bestConfigs = file["bestConfigs"]
                self.worstConfigs = file["worstConfigs"]
                file.close()
            else:
                file.close()
                self.generateDataCache(folder)
        else:
            self.generateDataCache(folder)

    # generiert das Cachefile
    def generateDataCache(self, folder):

        # erstellt eine json Liste für das Frontend mit den NFP-Namen
        for i in self.performance.nfpNames:
            # Leerzeichen herrausfiltern
            name = i.split("_")
            nameCap = ''
            j = 0
            while j < len(name):
                name[j] = name[j].capitalize()
                nameCap = nameCap + name[j]
                j = j + 1
                if j < len(name):
                    nameCap = nameCap + ' '

            # Isolieren der Maßeinheit
            name = nameCap.split("(")
            name[1] = name[1].strip(";<>)(")

            # Config für Start generieren
            options = [0] * len(self.feature.names)
            numerics = []
            stats = [sys.float_info.max] * len(self.performance.nfpNames)

            for m in self.feature.numericNames:
                numerics.append(m[2])
            config = Config(options=options, numeric=numerics)
            # Config optimieren für ein NFP fürs minimale zu finden
            (mincon, minstats) = self.optimize(config, stats, 0,
                                               (len(self.feature.names) + len(self.feature.numericNames)),
                                               self.performance.nfpNames.index(i), True, False, False)
            stats = [0] * len(self.performance.nfpNames)

            # Config optimieren um das maximale eines NFP´s zu finden
            (maxcon, maxstats) = self.optimize(config, stats, 0,
                                               (len(self.feature.names) + len(self.feature.numericNames)),
                                               self.performance.nfpNames.index(i), True, False, True)

            # Speichern des Eintrages in den Listen
            self.nfpJson.append({"name": i, "display_name": name[0], "unit": name[1],
                                 "minimum": minstats[self.performance.nfpNames.index(i)],
                                 "maximum": maxstats[self.performance.nfpNames.index(i)]})
            self.bestConfigs.append({"display_name": name[0], "code": mincon.getCode()})
            self.worstConfigs.append({"display_name": name[0], "code": maxcon.getCode()})

        # Berechnen der Variante über alle NFP´s
        options = [0] * len(self.feature.names)
        numerics = []
        stats = [sys.float_info.max] * len(self.performance.nfpNames)
        for m in self.feature.numericNames:
            numerics.append(m[2])
        config = Config(options=options, numeric=numerics)
        # Config optimieren für ein NFP fürs minimale zu finden
        (mincon, minstats) = self.optimize(config, stats, 0, (len(self.feature.names) + len(self.feature.numericNames)),
                                           'all', True, False, False)
        stats = [0.000000000001] * len(self.performance.nfpNames)

        # Config optimieren um das maximale eines NFP´s zu finden
        (maxcon, maxstats) = self.optimize(config, stats, 0, (len(self.feature.names) + len(self.feature.numericNames)),
                                           'all', True, False, True)

        # Speichern des Eintrages in den Listen
        self.bestConfigs.append({"display_name": 'All', "code": mincon.getCode()})
        self.worstConfigs.append({"display_name": 'All', "code": maxcon.getCode()})

        # Erstellte Json und Configs in Datei speichern
        saveFile = shelve.open(os.path.dirname(__file__) + '/../data/' + folder + "/data_cache.slv")
        saveFile["nfpJson"] = self.nfpJson
        saveFile["bestConfigs"] = self.bestConfigs
        saveFile["worstConfigs"] = self.worstConfigs
        saveFile.close()
