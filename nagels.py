import math

class VerbindingNagels():
    def __init__(self, verbindingsmiddel):
        eigenschap = verbindingsmiddel['Eigenschappen']
        self.verbinding_type = ['Type']
        self.nagel_type = eigenschap['Uitvoering']
        self.nagel_kop = eigenschap['Kop']['Type']
        self.nagel_diameter = eigenschap['Diameter']
        self.treksterkte = eigenschap['Treksterkte']
        self.Fax = eigenschap['Fax']
        self.Fhead = eigenschap['Fhead']
        self.kop_type = eigenschap['Kop']['Type']
        self.kop_diameter = eigenschap['Kop']['Diameter']
        self.moment_vloei = self.vloeimoment()


    def K90(self, element):
        if element['Soort'] == 'Naaldhout':
            K_90 =  1.35 + 0.015 * self.nagel_diameter
        elif element['Soort'] == 'LVL':
            K_90 = 1.30 + 0.015 * self.nagel_diameter
        elif element['Soort'] == 'Loofhout':
            K_90 = 0.90 + 0.015 * self.nagel_diameter
        else:
            K_90 = 'factor K90: verkeerde houtsoort'

        return K_90


    def checkVoorboring(self, verbindingstype, element1, element2):
        if self.nagel_diameter > 8:
            voorgeboord = True
        elif verbindingstype == 'Hout-op-hout':
            dikte = min(element1['Dikte'], element2['Dikte'])
            d1 = 7 * self.nagel_diameter
            d2 = (13 * self.nagel_diameter) * (min(element1['Ro'], element2['Ro']) / 400)
            dikte_toets = max(d1, d2)
            if dikte < dikte_toets:
                voorgeboord = True
            else:
                voorgeboord = False
        elif verbindingstype == 'Plaat-op-hout':
            if element1['Ro'] > 500 or element2['Ro'] > 500:
                voorgeboord = True
            else:
                voorgeboord = False
        elif verbindingstype == 'Staal-op-hout':
            if element1['Soort'] == 'Staal':
                if element2['Ro'] > 500:
                    voorgeboord = True
                else:
                    voorgeboord = False
            elif element2['Soort'] == 'Staal':
                if element1['Ro'] > 500:
                    voorgeboord = True
                else:
                    voorgeboord = False
        else:
            voorgeboord = False

        return voorgeboord


    def vloeimoment(self):
        if self.nagel_kop == 'Rond':
            vloeimoment = 0.3 * self.treksterkte * self.nagel_diameter**2.6
        elif self.nagel_kop == 'Vierkant' or self.nagel_kop == 'Geprofileerd':
            vloeimoment = 0.45 * self.treksterkte * self.nagel_diameter**2.6
        else:
            vloeimoment = 'verkeerde type nagelkop'

        return vloeimoment


    def stuiksterkteHout(self, verbindingstype, element1, element2, verbindingskrachten):
        voorgeboord = self.checkVoorboring(verbindingstype, element1, element2)
        if verbindingstype == 'Plaat-op-hout':
            if self.kop_diameter >= 2 * self.nagel_diameter:
                plaat = element1['Soort']
                if plaat == 'Multiplex':
                    stuiksterkte = 0.11 * element1['Ro'] * self.nagel_diameter ** (-0.3)
                elif plaat == 'Spaanplaat' or plaat == 'OSB':
                    stuiksterkte = 65 * self.nagel_diameter ** (-0.7) * element1['Dikte'] ** 0.1
                elif plaat == 'Hardboard':
                    stuiksterkte = 30 * self.nagel_diameter ** (-0.3) * element1['Dikte'] ** 0.6
                else:
                    stuiksterkte = 'element 1 moet plaat zijn van de soort Multiplex/Spaanplaat/OSB/Hardboard'
            else:
                stuiksterkte = 'kopdiameter moet ten minste 2*diameter zijn'
        else:
            stuiksterkte_min = list()
            for element in [element1, element2]:
                if element['Soort'] != 'Staal':
                    if self.nagel_diameter <= 8:
                        if voorgeboord == False:
                            stuiksterkte_min.append(0.082 * element['Ro'] * self.nagel_diameter**(-0.3))
                        if voorgeboord == True:
                            stuiksterkte_min.append(0.082 * (1 - 0.01 * self.nagel_diameter) * element['Ro'])
                    elif self.nagel_diameter > 8:
                        K_90 = self.K90(element)
                        stuiksterkte_even = 0.082 * (1 - (0.01 * self.nagel_diameter)) * element['Ro']
                        stuik = stuiksterkte_even / ((K_90 * (math.sin(verbindingskrachten['Rad']))**2) + (math.cos(verbindingskrachten['Rad']))**2)
                        stuiksterkte_min.append(stuik)
                else:
                    pass
            stuiksterkte = min(stuiksterkte_min)

        return stuiksterkte

    def uittreksterkte(self, element1, element2):
        if self.nagel_type == 'Glad':
            hechtlengte = element2['Hechtlengte']
            if hechtlengte < 8 * self.nagel_diameter:
                print('VW: Hechtlengte puntzijde ten minste 8d')
            elif hechtlengte >= 12 * self.nagel_diameter:
                Fax = 20 * 10**(-6) * element1['Ro']**2
                Fhead = 70 * 10**(-6) * element1['Ro']**2
                factor = 1
            else:
                factor = (hechtlengte / ((4 * self.nagel_diameter) - 2))
                Fax = self.Fax
                Fhead = self.Fhead
            F1 = Fax * self.nagel_diameter * hechtlengte
            F2 = Fax * self.nagel_diameter * element1['Dikte'] + Fhead * self.kop_diameter**2
            uittreksterkte = (min(F1, F2) * factor)


        elif self.nagel_type == 'Schroefdraad':
            hechtlengte = element2['Hechtlengte']
            if hechtlengte < (6 * self.nagel_diameter):
                print('hechtlengte in het element die de puntzijde bevat moet ten minste 6d zijn')
            elif hechtlengte < (8 * self.nagel_diameter):
                factor = (hechtlengte / ((2 * self.nagel_diameter) - 3))
            else:
                factor = 1
            F1 = self.Fax * self.nagel_diameter * hechtlengte
            F2 = self.Fhead * self.kop_diameter ** 2

            uittreksterkte = (min(F1, F2) * factor)
        else:
            uittreksterkte = 'VW: Type moet glad/schroefdraad zijn'

        return uittreksterkte


