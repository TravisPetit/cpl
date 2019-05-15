import cpl

def possible_interpretations(*indexes):
    propositions = [cpl.Proposition(index=indx) for indx in indexes]
    propositions.sort()
    interpretations = []

    # count to 2^n
    for i in range(2**len(indexes)):
        dict_ = {}

        for j in range(len(indexes)):
            # if i is divisible by 2, 4, 8, 16, ... that's wrong! you should check whether the digit at position * is a 0 or 1!
            #if i % ( 2 ** (j+1) ) == 0:
            #    dict_[propositions[j]] = False
            #else:
            #    dict_[propositions[j]] = True
            #dict_[propositions[j]] = bool(i & (2 ** (j+1)))
            dict_[propositions[j]] = bool(i & (2 ** j))

        inter = cpl.Interpretation(dict_)
        interpretations.append(inter)

    return interpretations
