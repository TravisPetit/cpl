import cpl
from random import random, randint, choice

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


def random_interpretation(*indexes):
    indexes = set(indexes)
    propositions = [cpl.Proposition(index=indx) for indx in indexes]
    propositions.sort()

    dict_ = {}
    for j in range(len(indexes)):
        dict_[propositions[j]] = choice([True,False])

    return cpl.Interpretation(dict_)



def random_formula(chance=0.70):
    counter = 0
    x = cpl.Proposition(index=counter)

    if random() < 0.5:
        x = -x

    while (random() < chance):
        counter += 1
        y = cpl.Proposition(index=max(randint(counter-2, counter+2),0))

        if random() < 0.5:
            y = -y

        if random() < 0.5:
            x = x + y
        else:
            x = x * y

    return x

def TT(n):
    x = [cpl.Proposition(index=i) for i in range(n)]
    res = [  x[0], HA_sum(x[1], x[0])  ]
    carrys = [ HA_cout(x[1], x[0]) ]

    for i in range(2, len(x)):
        #FAc = carrys[-1]
        FAc = FA_sum(x[i-1], x[i-2], carrys[-1])
        digit = FA_sum(x[i], x[i-1], FAc)

        carrys.append(FAc)
        res.append(digit)

    return res


def number_to_interpretation(n):
    q = str(bin(n))[2:][::-1]
    x = [cpl.Proposition(index=i) for i in range(len(q))]
    dict_ = {}

    for i in range(len(q)):
        dict_[x[i]] = (q[i] == "1")

    return cpl.Interpretation(dict_)


def interpretation_to_number(interpretation):
    x = sorted(interpretation.keys())
    num = 0
    for i in range(len(x)):
        if interpretation.evaluate(x[i]):
            num += 2 ** i
    return num
