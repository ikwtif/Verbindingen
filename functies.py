from pprint import pprint


def koordEffectBeperking(delen, beperking, koordeffect):
    koordeffect_beperkt = []
    for johansen in delen:
        laagste = min(johansen * beperking, koordeffect)
        koordeffect_beperkt.append(laagste)
    return koordeffect_beperkt


def koordEffectBeperkt(types, verbindingsmiddel):
    beperking_koordeffect = {'Nagels': {'Rond': 0.15,
                                        'Vierkant': 0.25,
                                        'Geprofileerd': 0.25,
                                        'Andere': 0.50},
                             'Schroeven': 1,
                             'Bouten':0.25,
                             'Stiften':0}

    if types == 'Nagels':
        kop = verbindingsmiddel['Eigenschappen']['Kop']['Type']
        beperking = beperking_koordeffect[types][kop]
    else:
        beperking = beperking_koordeffect[types]

    return beperking


def afschuivingHoH(snede, verbindingsmiddel, stuiksterkte_1k, stuiksterkte_2k, uittreksterkte, vloeimoment, element1, element2, element3=None):
    """
    NBN EN 1995-1-1:2005+AC:2006
    8.2 Sterkte van op afschuiving belaste stiftvormige metalen verbindingsmiddelen
    8.2.2 Hout-op-hout en plaat-op-houtverbindingen
    """
    # Setup variabelen
    print(element1, element2)
    element1_dikte = element1['Hechtlengte']
    element2_dikte = element2['Hechtlengte']
    if element3 != None:
        element3_dikte = element3['Hechtlengte']
    types = verbindingsmiddel['Type']
    diameter = verbindingsmiddel['Eigenschappen']['Diameter']
    koordeffect = uittreksterkte / 4

    Beta = stuiksterkte_2k / stuiksterkte_1k

    # Bepalen beperking koordeffect
    beperking = koordEffectBeperkt(types, verbindingsmiddel)


    if snede == 'Enkelsnedig':
        johansen_a = stuiksterkte_1k * element1_dikte * diameter

        johansen_b = stuiksterkte_2k * element2_dikte * diameter

        johansen_c = ((stuiksterkte_1k * element1_dikte * diameter) / (1 + Beta)) * \
                     ((Beta + (2 * Beta**2 * (1+(element2_dikte/element1_dikte)+(element2_dikte/element1_dikte)**2)) + Beta**3 * (element2_dikte/element1_dikte)**2)**(1/2) -
                      Beta * (1 + (element2_dikte/element1_dikte)))

        johansen_d = 1.05 * ((stuiksterkte_1k * element1_dikte * diameter)/(2 + Beta)) * \
                     (((2 * Beta * (1 + Beta))+((4 * Beta * (2 + Beta) * vloeimoment)/(stuiksterkte_1k*diameter*element1_dikte**2)))**(1/2) - Beta)

        johansen_e = 1.05 * ((stuiksterkte_1k * element2_dikte * diameter)/(1 + (2 * Beta))) * \
                     (((2 * (Beta**2) * (1 + Beta))+((4 * Beta * (1 + (2*Beta)) * vloeimoment)/(stuiksterkte_1k*diameter*element2_dikte**2)))**(1/2) - Beta)

        johansen_f = 1.15 * ((2 * Beta ) / (1 + Beta)) * (2 * vloeimoment * stuiksterkte_1k * diameter)**(1/2)

        delen = [johansen_c, johansen_d, johansen_e, johansen_f]
        koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)

        sterkte = [johansen_a, johansen_b]
        for i, johansen in enumerate(delen):
            sterkte.append(johansen + koordeffect_beperkt[i])

        Fvrx = sterkte[sterkte.index(min(sterkte))]

    if snede == 'Dubbelsnedig':
        if types == 'Nagels' and element3:
            element1_dikte = min(element1_dikte, element3['Hechtlengte'])


        johansen_g = stuiksterkte_1k * element1_dikte * diameter

        johansen_h = 0.5 * stuiksterkte_2k * element2_dikte * diameter

        johansen_i = 1.05 * ((stuiksterkte_1k * element1_dikte * diameter)/(2 + Beta)) * \
                     ((((2 * Beta) * (1 + Beta)) + ((4 * Beta * (2 + Beta) * vloeimoment) / (stuiksterkte_1k * element1_dikte**2)))**(1/2) - Beta)

        johansen_k = 1.15 * ((2 * Beta)/(1 + Beta))**(1/2) * (2 * vloeimoment * stuiksterkte_1k * diameter)**(1/2)

        delen = [johansen_i, johansen_k]
        koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)

        sterkte = [johansen_g, johansen_h]
        for i, johansen in enumerate(delen):
            sterkte.append(johansen + koordeffect_beperkt[i])

        Fvrx = sterkte[sterkte.index(min(sterkte))]

    saveLocals(locals(), 'AfschuivingHoH')
    return Fvrx


def afschuivingSoH(snede, element1, element2, verbindingsmiddel, stuiksterkte, uittreksterkte, vloeimoment):
    """
        NBN EN 1995-1-1:2005+AC:2006
        8.2 Sterkte van op afschuiving belaste stiftvormige metalen verbindingsmiddelen
        8.2.3 Staal-op-houtverbindingen
    """
    # stuiksterkte moet van houten element komen
    types = verbindingsmiddel['Type']
    koordeffect = uittreksterkte / 4
    diameter = verbindingsmiddel['Eigenschappen']['Diameter']

    beperking = koordEffectBeperkt(types , verbindingsmiddel)

    if element1['Soort'] == 'Staal':
        staalplaat_dikte = element1['Dikte']
        hout_dikte = element2['Dikte']
    elif element2['Soort'] == 'Staal':
        staalplaat_dikte = element2['Dikte']
        hout_dikte = element1['Dikte']

    if staalplaat_dikte <= 0.5 * diameter:
        staalplaat = 'Dun'
    elif staalplaat_dikte >= diameter:#en p71
        staalplaat = 'Dik'
    else:  # interpoleren
        staalplaat = 'Both'


    if snede == 'Enkelsnedig' and element1['Soort'] == 'Staal':
        if staalplaat == 'Dun':
            #stuiksterkte moet van houten element komen
            johansen_a = 0.4 * stuiksterkte * hout_dikte * diameter
            johansen_b = 1.15 * (2 * vloeimoment * stuiksterkte * diameter)**(0.5)
            delen = [johansen_b]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [johansen_a]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])
            Fvrx = sterkte[sterkte.index(min(sterkte))]

        if staalplaat == 'Dik':
            johansen_c = stuiksterkte * hout_dikte * diameter * \
                         ((2 + (4 * vloeimoment)/(stuiksterkte * diameter * hout_dikte**2))**0.5-1)
            johansen_d = 2.3 * (vloeimoment * stuiksterkte * diameter)**0.5
            johansen_e = stuiksterkte * hout_dikte * diameter
            delen = [johansen_c, johansen_d]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [johansen_e]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])
            Fvrx = sterkte[sterkte.index(min(sterkte))]

    elif snede == 'Dubbelsnedig':
        if element2['Soort'] == 'Staal':
            johansen_f = stuiksterkte * hout_dikte * diameter
            johansen_g = stuiksterkte * hout_dikte * diameter * \
                         (((2 + (4 * vloeimoment)/(stuiksterkte * diameter * hout_dikte**2))**0.5)-1)
            johansen_h = 2.3 * (vloeimoment * stuiksterkte * diameter)**0.5
            delen = [johansen_g, johansen_h]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [johansen_f]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])

            Fvrx = sterkte[sterkte.index(min(sterkte))]

        if staalplaat == 'Dun' and element1['Soort'] == 'Staal':
            jh_1 = 0.5 * stuiksterkte * hout_dikte * diameter
            print('stuiksterkte:', stuiksterkte, 'houtdikte:', hout_dikte, 'diameter', diameter)
            jh_2 = 1.15 * (2 * vloeimoment * stuiksterkte * diameter)**0.5
            delen = [jh_2]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [jh_1]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])
            Fvrx = sterkte[sterkte.index(min(sterkte))]


        if staalplaat == 'Dik' and element1['Soort'] == 'Staal':
            jh_3 = 0.5 * stuiksterkte * hout_dikte * diameter
            jh_4 = 2.3 * (vloeimoment * stuiksterkte * diameter)**0.5
            delen = [jh_4]
            koordeffect_beperkt = koordEffectBeperking(delen, beperking, koordeffect)
            sterkte = [jh_3]
            for i, johansen in enumerate(delen):
                sterkte.append(johansen + koordeffect_beperkt[i])

            Fvrx = sterkte[sterkte.index(min(sterkte))]

    saveLocals(locals(), 'AfschuivingSoH')
    pprint(locals())
    return Fvrx


def saveLocals(output, text):
    with open('{}.txt'.format(text), 'wt') as out:
        pprint(output, stream=out)
