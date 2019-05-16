import cpl
from random import random, randint

HA_sum = lambda x,y : (-x)*y + x*(-y)
HA_cout = lambda x,y : x*y

FA_sum = lambda x,y,cin : (-x)*(-y)*cin + (-x)*y*(-cin) + x*(-y)*(-cin) + x*y*cin
FA_cout = lambda x,y,cin : y*cin + x*cin + x*y

def possible_interpretations(*indexes):
    indexes = set(indexes)
    propositions = [cpl.Proposition(index=indx) for indx in indexes]
    propositions.sort()
    interpretations = []

    for i in range(2**len(indexes)):
        dict_ = {}

        for j in range(len(indexes)):
            dict_[propositions[j]] = bool(i & (2 ** j))

        inter = cpl.Interpretation(dict_)
        interpretations.append(inter)

    return interpretations



def statisfiable(formula):
    for interpretation in possible_interpretations(*formula.indexes_involved):
        if interpretation.evaluate(formula):
            return True, interpretation

    return False, cpl.Interpretation({})


def random_formula(chance=0.70):
    counter = 0
    x = cpl.Proposition(index=randint(0, counter+1))

    if random() < 0.5:
        x = -x

    while (random() < chance):
        counter += 1
        y = cpl.Proposition(index=counter)

        if random() < 0.5:
            y = -y

        if random() < 0.5:
            x = x + y
        else:
            x = x * y

    return x
