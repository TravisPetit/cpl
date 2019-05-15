import cpl

def possible_interpretations(*indexes):
    indexes = set(indexes)
    propositions = [cpl.Proposition(index=indx) for indx in indexes]
    propositions.sort()
    interpretations = []

    # count to 2^n
    for i in range(2**len(indexes)):
        dict_ = {}

        for j in range(len(indexes)):
            dict_[propositions[j]] = bool(i & (2 ** j))

        inter = cpl.Interpretation(dict_)
        interpretations.append(inter)

    return interpretations
