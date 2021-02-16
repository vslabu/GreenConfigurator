import base64
from sys import byteorder
from math import ceil


# Klasse config
# Methoden :    Konstruktor
#               getClosest
#               getLink
class Config():
    # speichert die Konfiguration, vom Typ boolean
    options = []
    numeric = []

    # anzahl der benutzten bytes
    length = 0

    # die Anzahl von Zeichen, die im Link für die Angabe der Länge verwendet werden
    minLength = 2

    # Konstruktor bekommt einen Link einer Konfiguration übergeben
    # oder eine Liste von Optionen
    # String link einer Konfiguration
    # das erste zeichen von Link gibt an, wie viele Nullen gepaddet wurden
    # die minLength Zeichen danach von link geben die Länge an
    def __init__(self, code='', options=[], numeric=[]):
        # wenn ein link als input gegeben ist
        if code:
            # überprüfe ob link lang genug
            if len(code) <= self.minLength + 2:
                raise Exception('Link too short')
            else:
                numLink, opLink = code.split('.', 1)
                if numLink:
                    self.numeric = [int(i) for i in numLink.split(':')]
                else:
                    self.numeric = []
                pad = int(opLink[0])
                self.length = int(opLink[1:1 + self.minLength])
                bytes_as_int = int.from_bytes(base64.urlsafe_b64decode(opLink[1 + self.minLength:]), byteorder)
                bitstring = '{0:b}'.format(bytes_as_int)
                # padde nullstellen links, entferne pad nullstellen
                padded = bitstring.rjust((8 - len(bitstring) % 8) + len(bitstring), '0')[pad:]
                self.options = [int(i) for i in padded]
        # wenn eine Konfiguration von gegebenen Optionen generiert werden soll    
        elif (options):
            self.options = options
            self.numeric = numeric
            self.length = ceil(len(options) / 8)
        else:
            raise Exception('Kann keine leere Konfiguration erstellen!')

    # Zwei Configs können geordnet werden
    def __ge__(a, b):
        if len(a.options) != len(b.options):
            raise Exception('Konfigurationen sind unterschiedlich groß!')
        else:
            res = True
            for x, y in zip(a.options, b.options):
                if y > x:
                    res = False
                    break
            return res

    # gibt einen Link einer Konfiguration zurück
    # @return String der Link enthält
    def getCode(self):
        l = ':'.join(map(str, self.numeric)) + '.'
        # Dieser Code nutzt, dass True=1, False=0 in python
        # << ist bitwise shift, d.h. de facto 2^v
        s = sum(v << i for i, v in enumerate(reversed(self.options)))
        # s zu length bytes mit default-byteorder des Systems
        res = s.to_bytes(self.length, byteorder)
        # decode, damit b gleich string ist 
        b = base64.urlsafe_b64encode(res).decode("utf-8")
        # wie viel padding (also ungenutzte nullstellen links?). muss unter 8 sein
        pad = self.length * 8 - len(self.options)
        if pad > 8:
            raise Exception('Cannot pad properly, link too large')
        return l + str(pad) + str(self.length).rjust(self.minLength, '0') + b

    # Generiert die Configs, welche sich maximal um den Wert x von der gegebenen Config unterscheidet
    # @param int x für den Grad der Nähe
    # @return boolean[] Config
    # TODO: effizienz
    def getClosest(self, x):
        current = {tuple(map(bool, self.options))}
        whole = current.copy()

        for i in range(0, x):
            current = self.onlyOne(current)
            whole = whole.union(current)
            if len(whole) == 2 ** len(self.options):
                break

        # numeric wird erstmal nicht abgeändert
        return map(lambda e: Config(options=list(e), numeric=self.numeric), whole)


    # Hilfsfunktion für getClosest
    def onlyOne(self, current):
        s = set()
        for o in current:
            for i in range(0, len(self.options)):
                cp = list(o)
                cp[i] = not cp[i]
                s.add(tuple(cp))
        return s

    def toJson(self, model):
        names = model.feature.names
        numNames = model.feature.numericNames

        res = []

        for i, o in enumerate(self.options):
            res.append({'name': names[i][1], 'id': i, 'enabled': bool(o)})
        for i, o in enumerate(self.numeric):
            res.append({'name': numNames[i][1], 'id': int(numNames[i][0]) - 1, 'value': o})


        return res


def jsonToConfig(json, n):
    # Erstellt array von booleans aus der empfangenen json Datei
    optionList = [0] * n
    numericList = [0] * (len(json) - n)

    # übernimmt die gesetzten Features als Konfiguration
    for f in json:
        if f.get('enabled'):
            optionList[int(f.get('id'))] = 1
        elif f.get('value'):
            numericList[int(f.get('id')) - n] = f.get('value')

    # gibt ein Config-Objekt zurück
    return Config(options=optionList, numeric=numericList)
