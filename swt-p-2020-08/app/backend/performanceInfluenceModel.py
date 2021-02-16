from config import Config
import os


# Klasse PerformanceInfluenceModel
# Methoden :    Konstruktor
#               getStats

# speichert und berechnet das PerformanceInfluenceModel
class PerformanceInfluenceModel:
    # Konstruktor der Klasse
    # speichert das PIM
    # @param perf nimmt die CSV-Datei(Namen) zum Einlesen
    def __init__(self, feat, perf="model", folder="HSQL DB"):

        self.fm = feat

        # speichert die Namen von NFP
        self.nfpNames = []

        # speichert die Anzahl von NFP in der CSV
        self.nfpNumber = 0

        # speichert die Berechnungsmodelle
        self.model = []

        try:
            # file öffnen und Zeilenweise einlesen
            file = open(os.path.dirname(__file__) + '/../data/' + folder + "/" + perf + '.csv', "r")
            for x in file:
                # ein gelesene Zeile zerlegen
                line = x.split(",")
                line[len(line) - 1] = line[len(line) - 1].replace("\n", "")

                # Aufteilen der Zeilen nach Namen und Regeln
                if line[0] == 'root':
                    # namen der nfps (wir lesen die Namen der Features nicht mit!)
                    self.nfpNames = line[(len(self.fm.names) + len(self.fm.numericNames)):]
                    # Anzahl der NFP in CSV
                    self.nfpNumber = len(self.nfpNames)

                else:
                    # liest die nicht-NFP-Einträge (also die Konfiguration) als ints
                    opts = [int(i) for i in line[0:len(self.fm.names)]]
                    nums = [int(i) for i in line[len(self.fm.names):len(self.fm.names) + len(self.fm.numericNames)]]
                    conf = Config(options=opts, numeric=nums)
                    nfps = list(map(float, line[len(line) - self.nfpNumber:]))
                    # Das PI-Modell besteht aus (Sub-)Konfigurationen, denen NFPs zugewiesen sind
                    self.model.append((conf, nfps))
        except FileNotFoundError:
            raise Exception("Datei nicht vorhanden")
        file.close()

    # gibt die NFP-Points zu einer Konfiguration zurück
    # @param con ist eine korrekte Konfiguration
    # @return gibt die berechneten NFP-Points zurück
    def getStats(self, con):
        # delete value for a second run
        nfpValue = [0] * self.nfpNumber

        # sucht relevante Zeilen
        for (c, nfp) in self.model:
            if c <= con:
                multiplier = sum([val * con.numeric[i] for i, val in enumerate(c.numeric)])
                multiplier = multiplier if multiplier else 1
                for k in range(0, self.nfpNumber):
                    nfpValue[k] = nfpValue[k] + nfp[k] * multiplier
        return nfpValue

    # gibt die NFP-Points zu einer Konfiguration zurück
    # @param con ist eine korrekte Konfiguration
    # @return gibt die berechneten NFP-Points zurück
    def getSingleStats(self, con):
        # delete value for a second run
        nfpValue = [0] * self.nfpNumber
        singlefeats = []
        i = 0
        # Einzelliste
        while i < len(self.fm.names)+len(self.fm.numericNames):
            if i < len(self.fm.names):
                name = self.fm.names[i][1]
            else:
                name = self.fm.numericNames[i - len(self.fm.names)][1]
            singlefeats.append((i, nfpValue.copy(), name))
            i = i + 1

        # sucht relevante Zeilen
        for (c, nfp) in self.model:
            if c <= con:
                # sucht in der Liste nach den Featurenummern die zutreffen und merkt sich diese Features
                activefeatures = []
                i = 0
                while i < (len(self.fm.names)+len(self.fm.numericNames)):
                    if i < len(self.fm.names):
                        if c.options[i]:
                            activefeatures.append(i)
                    else:
                        if c.numeric[i-len(self.fm.names)]:
                            activefeatures.append(i)
                    i = i + 1


                multiplier = sum([val * con.numeric[i] for i, val in enumerate(c.numeric)])
                multiplier = multiplier if multiplier else 1
                #Aufteilen der NFPs auf die entsprechenden Features anteilig auf die entsprechenden Features
                for j in activefeatures:
                    for k in range(0, self.nfpNumber):
                        singlefeats[j][1][k] = singlefeats[j][1][k] + nfp[k] * multiplier / len(activefeatures)

        # leere Features entfernen
        i = 0
        while i < len(singlefeats):
            if singlefeats[i][1] == nfpValue:
                singlefeats.remove(singlefeats[i])
            else:
                i = i + 1

        return singlefeats
