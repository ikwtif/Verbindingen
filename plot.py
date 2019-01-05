from nagels import VerbindingNagels
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


db = {'Verbinding': {'Type': 'Hout-op-hout',
                     'Snede': 'Enkelsnedig',
                     'Element 1': {'Dikte': 71,
                                   'Ro': 320,
                                   'Kmod': 0.9,
                                   'Soort': 'Loofhout',
                                   'Hechtlengte': 71},
                     'Element 2': {'Dikte': 35,
                                   'Ro': 320,
                                   'Kmod': 0.9,
                                   'Soort': 'Loofhout',
                                   'Fc': 2.2,
                                   'Hechtlengte': 29}
                     },
      'Verbindingsmiddel': {'Type': 'Nagels',
                            'Eigenschappen': {'Uitvoering': 'Glad',
                                              'Kop': {'Type': 'Rond',
                                                      'Diameter': 3},
                                              'Diameter': 7,
                                              'Treksterkte': 235,
                                              'Lengte': 100,
                                              'Fax': 2.05,
                                              'Fhead': 7.17}},
      'Verbindingskrachten': {'Alfa': 1.57,
                              'AlfaTrek': 0,
                              'Rad': 1.57,
                              'RadTrek': 0
                              }
      }


element1 = db['Verbinding']['Element 1']
element2 = db['Verbinding']['Element 2']
verbindingsmiddel = db['Verbindingsmiddel']
verbindingskrachten = db['Verbindingskrachten']

nagel = VerbindingNagels(verbindingsmiddel)
nagel.stuiksterkteHout('Hout-op-hout', 'Enkelsnedig', element1, element2, verbindingskrachten)


variabele1n = 'nagel diameter'
variabele1 = nagel.nagel_diameter
kracht = []
variabele = []
try:
    i = 0
    while i < 100:
        kr = nagel.uittreksterkte(element2, element1)
        nagel.nagel_diameter += 0.1
        kracht.append(kr)
        variabele.append(nagel.nagel_diameter)
        i += 1
except:
    pass
xas = variabele
yas = kracht

print(xas)
print(yas)

fig, ax = plt.subplots()
ax.plot(yas, xas)
ax.set(xlabel='uittreksterkte', ylabel=variabele1n, title='')
ax.grid()
fig.savefig(variabele1n)
plt.show()