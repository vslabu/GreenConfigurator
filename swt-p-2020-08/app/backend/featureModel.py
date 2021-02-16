from bs4 import BeautifulSoup
import os
import xmltodict
import json


# Klasse featureModel
# Methoden :    Konstruktor
#               validate
#               angepassteXML
#               generateFeaturetree
#               configJson
#               allwoedValues

# speichert das Featuremodel und führt die Validierung aus
class FeatureModel:

    # Klassenkonstruktor
    # @param feat bekommt DIMAC-Dateinnamen übergeben, zum Einlesen und liest das File dann ein
    # feat = FeatureModel zum Setzen von FeatureModel.DIMACS als Standard-Datei
    # wird komplett in model gespeichr
    def __init__(self, feat="FeatureModel", xml="FeatureModel", folder="HSQL DB"):

        # speichert die Regeln in KNF
        self.rules = []

        # erlaubte numerische Werte
        self.numericValues = []

        # speichert die einzelnen Features  [feature1, feature2, ...]
        self.names = []

        # speichert die XML in einer Json-Datei
        self.xmlInJSon = ''

        # neue angepasste XML Datei
        self.angepassteJson = ''

        # Liste numeric options
        # beinhaltet [Featurenummer, Featurename, MinValue, MaxValue, Stepsize, Operator]
        self.numericNames = []

        # speichert eine Config Liste zur Übertragung fürs Frontend
        self.configurationList = []

        try:
            # DIMACS-file öffnen und Zeilenweise bearbeiten
            file = open(os.path.dirname(__file__) + '/../data/' + folder + "/" + feat + '.dimacs', "r")
            for x in file:
                # ein gelesene Zeile zerlegen
                line = x.split(" ")

                # Aufteilen der Zeilen nach Namen und Regeln
                if line[0] == 'c':
                    self.names.append([line[1], line[2].replace("\n", "")])
                elif line[0] == 'p':
                    pass
                else:
                    # beim letzen Element Zeilenumbruch enternen
                    line_int = []
                    line[len(line) - 1] = line[len(line) - 1].replace("\n", "")
                    i = 0
                    while i < len(line) - 1:
                        line_int.append(int(line[i]))
                        i = i + 1
                    self.rules.append(line_int)

            file.close()
        except FileNotFoundError:
            raise Exception("File nicht vorhanden")

        try:
            # XML-File öffnen und einlesen und umwandeln in json-Datei
            with open(os.path.dirname(__file__) + '/../data/' + folder + "/" + xml + '.xml', "r") as xmlFile:
                obj = xmltodict.parse(xmlFile.read())
            self.xmlInJSon = json.dumps(obj)
            xmlFile.close()
        except FileNotFoundError:
            raise Exception("File nicht vorhanden")

        self.angepassteXML(xml=xml, folder=folder)
        self.configJson()
        self.allowedValues()

    # prüft die Korrektheit der gewählten Konfiguration anhand der KNF-Regeln
    # @param con bekommt eine Konfiguration übergeben
    # @return gibt eine boolean für eine korrekte oder inkorrekte Konfiguration zurück
    def validate(self, config):
        # Aufspalten der Config auf zwei Variablen zur besseren Übersichtlichkeit
        booleanFeat = config.options
        numericFeat = config.numeric

        # prüft die Länge der Konfiguration, ob diese von der Anzahl der Werte korrekt ist
        if len(self.names) + len(self.numericNames) != len(booleanFeat) + len(numericFeat):
            raise Exception("The Config doesn't have the correct length!")
        else:

            # Durchlaufen der Regeln
            for i in self.rules:
                j = 0
                rule = False
                # Betrachten der Disjunktion
                while (j < len(i)) and (rule == False):
                    # Wenn an der Stelle der Parameter 1 sein muss
                    if (int(i[j]) > 0) and (booleanFeat[abs(i[j]) - 1] == 1):
                        rule = True
                    # Wenn an der Stelle der Parameter 0 sein muss
                    elif (int(i[j]) < 0) and (booleanFeat[abs(i[j]) - 1] == 0):
                        rule = True
                    j = j + 1

                # Prüfung ob Disjunktion erfüllt ist, wenn nicht return false
                if not rule:
                    return False

            # Prüfen ob die numerischen Werte in den Toleranzbereichen liegen
            # Prüfen ob sie die Schrittweite einhalten
            if len(self.numericNames) > 0:
                i = 0
                for num in self.numericNames:
                    rule = False
                    # Prüfen ob Wert in den Grenzen ist
                    if numericFeat[i] >= num[2] and numericFeat[i] <= num[3]:
                        j = self.numericValues[i]
                        # Prüfen ob der Wert erlaubt ist
                        if num[0] == j[0] and not rule and numericFeat[i] in j[1]:
                            rule = True
                        # TODO Stepsize überprüfen
                    if not rule:
                        return False
                    i = i + 1

            # komplette KNF erfüllt
            return True

    # liest die XML ein und generiert eine angepasste Json-Datei
    # nimmt das XML-File entgegen und den Ordnernamen
    def angepassteXML(self, xml="FeatureModel", folder="HSQL DB"):

        # angepasste XML-einlesen und aufbauen
        try:
            # XML-File öffnen und einlesen und umwandeln in json-Datei

            # XML File laden
            pfad = (os.path.dirname(__file__) + '/../data/' + folder + "/" + xml + '.xml')
            xml_parser = BeautifulSoup(open(pfad), 'xml')
        except FileNotFoundError:
            raise Exception("File nicht vorhanden")
            p
        # Name des Modells parsen
        model_name = xml_parser.vm
        model_name = model_name['name']

        # alle ConfigurationOptionen werden aus dem XML ausgelesen
        configurationOptions = xml_parser.findAll('configurationOption')

        # Speicherobjekt für die Features
        features = []

        # arbeitet die gesamten Features durch und generiert einen Baum
        # falls mehr als ein Objekt wie root existiert
        while len(configurationOptions) > 0:
            option = configurationOptions.pop(0)
            feature = self.generateFeaturetree(configurationOptions, option, True)
            features.append(feature)

        # speichern der angepassten Json
        self.angepassteJson = features

    # generiert einen Baum und fügt alle Kinder zu einem Objekt hinzu
    # configurationOptions ist die Liste die alle restlichen Optionen noch enthält
    # option aktuell zu bearbeitende Funktion
    # always_activated_parentOption übergibt, ob das Elternteil immer aktiv sein muss
    def generateFeaturetree(self, configurationOptions, option, always_activated_parentOption):

        # Namen des Features genrieren
        name = option.find('name').contents[0]
        capitalize_name = name.split("_")
        i = 0
        while i < len(capitalize_name):
            capitalize_name[i] = capitalize_name[i].capitalize()
            i = i + 1
        i = 0
        display_name = str(capitalize_name[i])
        i = i + 1
        while i < len(capitalize_name):
            display_name = str(display_name) + ' ' + str(capitalize_name[i])
            i = i + 1

        # ID des Features generieren
        id = ""
        counter = 0

        # Prüfen ob das Feature in den binären Featureliste enthalten ist
        while id == "" and counter < len(self.names):
            element = self.names[counter]
            if element[1] == name:
                id = counter
            counter = counter + 1

        # Wenn id nicht gesetzt ist, dann ist es ein numerisches Feature
        # Feature in die numerische Liste eintragen und id setzen und die ID setzen
        if id == "":
            id = counter + len(self.numericNames)

        # Type generieren
        type = ""
        minValue = None
        maxValue = None
        stepFunction = None
        outputString = None
        try:
            prefix = option.find('prefix').contents[0]
        except:
            prefix = '\n'
        postfix = None
        if prefix == '\n':
            type = "bool"
            prefix = None
            outputString = option.find('outputString').contents[0]
            if outputString == '\n':
                outputString = None
        else:
            type = "numeric"
            minValue = int(option.find('minValue').contents[0])
            maxValue = int(option.find('maxValue').contents[0])
            stepFunction = option.find('stepFunction').contents[0]

            # Isolieren von Operator und Schrittgröße und speichern der min, max und Schrittwerte und Operator zum numerischen Feature
            step = stepFunction.split(' ')
            self.numericNames.append([str(id+1), name, int(minValue), int(maxValue), int(step[2]), step[1]])
            try:
                postfix = option.find('postfix').contents[0]
            except:
                postfix = None

        # ExcludedOptions hinzufügen
        excluded = []
        excludedOptions = option.findAll('options')
        i = 0
        while len(excludedOptions) > i:
            excluded.append(str(excludedOptions[i].contents[0]))
            i = i + 1

        optional = False
        always_activated = False
        # Herrausfinden ob Optional
        if type == "bool":
            optional = option.find('optional').contents[0]
            if optional == 'True':
                optional = True
            else:
                optional = False

            if optional == False and always_activated_parentOption == True and len(excluded) == 0:
                always_activated = True

        # Children generieren
        children = []

        i = 0
        # Wenn noch Optionen verfügbar sind, prüfe, ob sie Kind von dieser Option sind
        while len(configurationOptions) > i:
            parent = configurationOptions[i].find('parent').contents[0]
            # Wenn eins entnommen und Rekursion gestartet, wird Zähler zurück gesetzt, da nicht bekannt,
            # wiviele Elemente entnommen wurden
            if parent == name:
                child = configurationOptions.pop(0)
                children.append(self.generateFeaturetree(configurationOptions, child, always_activated))
                i = 0
            # ansonsten Nachfolger betrachten
            else:
                i = i + 1

        # Childrentype bestimmen
        # Prüfen ob Children vorhanden sind
        if len(children) == 0:
            children_type = None
        # hat Children
        else:
            # Kindertyp auswerten
            children_type = "CHOOSE_MULTIPLE"

            if (len(children[0].get('excluded')) > 0) and children[0].get('optional') == False:
                children_type = "CHOOSE_ONE"
            elif (len(children[0].get('excluded')) > 0) and children[0].get('optional') == True:
                children_type = "CHOOSE_MAX_ONE"

        # Rückgabe der bearbeiteten Featureliste
        return {'id': id,
                'name': name,
                'display_name': display_name,
                'type': type,
                'minValue': minValue,
                'maxValue': maxValue,
                'stepFunction': stepFunction,
                'outputString': outputString,
                'prefix': prefix,
                'postfix': postfix,
                'optional': optional,
                'always_activated': always_activated,
                'excluded': excluded,
                'children': children,
                'children_type': children_type}

    # generiert Listen die für die Json im Frontend zur Initalisierung der Oberfläche genutzt werden
    # in diesem Fall ist es eine Vorlage für die Speicherung der Konfiguration
    def configJson(self):
        # Liste enthält alle Features und einen Defaultwert
        for i in self.names:
            self.configurationList.append({"name": i[1], "id": (int(i[0]) - 1), "enabled": False})

        for i in self.numericNames:
            self.configurationList.append({"name": i[1], "id": (int(i[0]) - 1), "value": i[2]})

    # speichert in einer Liste für die numerischen Werte die erlaubten Konfigurationswerte ab
    def allowedValues(self):
        for i in self.numericNames:
            value = i[2]
            liste = []
            while value <= i[3]:
                liste.append(value)
                if i[5] == '+':
                    value = value + i[4]
                elif i[5] == '*':
                    value = value * i[4]
                elif i[5] == '-':
                    value = value - i[4]
                else:
                    value = value / i[4]
            self.numericValues.append([i[0], liste])
