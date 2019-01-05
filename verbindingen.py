import functies
from nagels import VerbindingNagels
from pprint import pprint
from bouten import VerbindingBouten
#from schroeven import VerbindingSchroeven


class Verbindingen():
    """
    NBN EN 1995-1-1:2005+AC:2006 (NL)
    """
    def __init__(self, verbinding):
        self.verbindingstype = verbinding['Type']
        self.verbindingsnede = verbinding['Snede']
        self.element1 = verbinding['Element 1']
        self.element2 = verbinding['Element 2']
        if self.verbindingsnede == 'Dubbelsnedig':
            self.element3 = verbinding['Element 3']
        else:
            self.element3 = None



    def berekeningSterkte(self, verbindingsmiddel, verbindingskrachten):
        """
        8.1.2 Verbindingen met meer dan een verbindingsmiddel
        """
        Fv_ef = Nef * Fv_Rk

        afschuif_el1 = self.afschuivingElement(data)
        afschuif_el2 = self.afschuivingElement(data)

        return Fv_ef

    def snedig(self):
        # setup elementen enkelsnedig/dubbelsnedig
        if self.verbindingsnede == 'Enkelsnedig':
            pass
        elif self.verbindingsnede == 'Dubbelsnedig':
            pass
        pass

    def verbinding(self):

        pass

    def afschuivingElement(self, verbindingsmiddel, verbindingskrachten):
        """
        8.2 Sterkte van op afschuiving belaste stiftvormige metalen verbindingsmiddelen
        """
        #karakteristieke sterkte
        verbinding_type = verbindingsmiddel['Type']
        if verbinding_type == 'Nagels':
            verbinding_Func = VerbindingNagels(verbindingsmiddel)
            if self.element1['Soort'] == 'Staal':
                uittreksterkte = verbinding_Func.uittreksterkte(self.element1,
                                                            self.element2)
            elif self.element2['Soort'] == 'Staal':
                uittreksterkte = verbinding_Func.uittreksterkte(self.element2,
                                                            self.element1)
        elif verbinding_type == 'Bouten':
            verbinding_Func = VerbindingBouten(verbindingsmiddel)
            if self.element1['Soort'] == 'Staal':
                uittreksterkte = verbinding_Func.uittreksterkte(self.element1,
                                                            self.verbindingstype)
            elif self.element2['Soort'] == 'Staal':
                uittreksterkte = verbinding_Func.uittreksterkte(self.element2,
                                                            self.verbindingstype)

        if self.verbindingstype == 'Hout-op-hout' or self.verbindingstype == 'Plaat-op-hout':
            stuiksterkte1 = verbinding_Func.stuiksterkteHout(self.verbindingstype,
                                                             self.element1,
                                                             self.element2,
                                                             verbindingskrachten)
            stuiksterkte2 = verbinding_Func.stuiksterkteHout(self.verbindingstype,
                                                             self.element2,
                                                             self.element1,
                                                             verbindingskrachten)
            sterkte_kar = functies.afschuivingHoH(snede=self.verbindingsnede,
                                    element1=self.element1,
                                    element2=self.element2,
                                    element3=self.element3,
                                    verbindingsmiddel=verbindingsmiddel,
                                    stuiksterkte_1k=stuiksterkte1,
                                    stuiksterkte_2k=stuiksterkte2,
                                    uittreksterkte=uittreksterkte,
                                    vloeimoment=verbinding_Func.moment_vloei)

        elif self.verbindingstype == 'Staal-op-hout':
            # stuiksterkte bepalen enkel van houten deel
            if self.element1['Soort'] != 'Staal':
                stuiksterkte = verbinding_Func.stuiksterkteHout(verbindingstype=self.verbindingstype,
                                                                 element1=self.element1,
                                                                 element2=self.element2,
                                                                 verbindingskrachten=verbindingskrachten)
            elif self.element2['Soort'] != 'Staal':
                stuiksterkte = verbinding_Func.stuiksterkteHout(verbindingstype=self.verbindingstype,
                                                                 element1=self.element2,
                                                                 element2=self.element1,
                                                                 verbindingskrachten=verbindingskrachten)

            functies.afschuivingSoH(snede=self.verbindingsnede,
                                    element1=self.element1,
                                    element2=self.element2,
                                    verbindingsmiddel=verbindingsmiddel,
                                    stuiksterkte=stuiksterkte,
                                    uittreksterkte=uittreksterkte,
                                    vloeimoment=verbinding_Func.moment_vloei)

if __name__ == '__main__':
    from nagels import VerbindingNagels


    db = eval(open('SohDubbelNagelMidden.txt', 'r').read())

    verbinding = Verbindingen(db['Verbinding'])
    verbinding.afschuivingElement(db['Verbindingsmiddel'], db['Verbindingskrachten'])



