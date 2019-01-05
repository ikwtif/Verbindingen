import math


class VerbindingBouten():
    def __init__(self, verbindingsmiddel):
        eigenschap = verbindingsmiddel['Eigenschappen']
        self.bout_diameter = eigenschap['Diameter']
        self.treksterkte = eigenschap['Treksterkte']
        self.sterkte_sluitring = eigenschap['Sterkte sluitring']
        self.moment_vloei = 0.3 * self.treksterkte * self.bout_diameter ** 2.6
        self.voorgeboord = True


    def checkVoorboring(self):
        return self.voorgeboord


    def K90(self, element):#verbindingstype mag weg
        if element['Soort'] == 'Naaldhout':
            K_90 =  1.35 + 0.015 * self.bout_diameter
        elif element['Soort'] == 'LVL':
            K_90 = 1.30 + 0.015 * self.bout_diameter
        elif element['Soort'] == 'Loofhout':
            K_90 = 0.90 + 0.015 * self.bout_diameter
        else:
            K_90 = 'factor K90: verkeerde houtsoort'

        return K_90


    def stuiksterkteHout(self, verbindingstype, element1, element2, verbindingskrachten):
        if self.bout_diameter < 30:
            if verbindingstype == 'Hout-op-hout' or verbindingstype == 'Staal-op-hout': # 2de deel stuik???
                # element 1 in berekening moet hout zijn
                if element1['Soort'] == 'Staal':
                    element2 = element1
                    element1 = element2
                K_90 = self.K90(element1)
                stuiksterkte_even = 0.082 * (1 - (0.01 * self.bout_diameter)) * element1['Ro']
                stuiksterkte = stuiksterkte_even / ((K_90 * (math.sin(verbindingskrachten['Rad']))**2) +
                                                    (math.cos(verbindingskrachten['Rad']))**2)
            elif verbindingstype == 'Plaat-op-hout':
                plaat = element1['Soort']
                if plaat == 'Multiplex':
                    stuiksterkte = 0.11 * (1 - 0.01 * self.bout_diameter) * element1['Ro']
                elif plaat == 'Spaanplaat' or plaat == 'OSB':
                    # welke dikte gebruiken????
                    stuiksterkte = 50 * self.bout_diameter**(-0.6) * element1['Dikte']
                else:
                    stuiksterkte = 'element 1 moet plaat zijn van de soort Multiplex/Spaanplaat/OSB'

        return stuiksterkte


    def uittreksterkte(self, element, verbindingstype):
        if verbindingstype == 'Staal-op-hout':
            if element['Soort'] == 'Staal':
                kracht = min(self.treksterkte, element['Treksterkte'])
            else:
                kracht = 'Element soort moet staal zijn'
        else:
            kracht = min (self.treksterkte, self.sterkte_sluitring)

        return kracht
