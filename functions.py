import cpl
import math
from random import random, randint, choice
from copy import deepcopy
import qm

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


def truth_table(formula):
    t = ""
    for q in formula.indexes_involved:
        t += str(cpl.Proposition(index = q)) + " | "
    t += "\n"
    for i in range(len(t)-2):
        t += "-"
    t +="\n"
    for interpretation in possible_interpretations(*(formula.indexes_involved)):
        t += " "
        nu = interpretation_to_number(interpretation)
        nu = str(bin(nu))[2:]
        for i in range(len(nu),len(formula.indexes_involved)):
            nu = "0" + nu
        for char in nu:
            t += char + "    "

        t += "| "
        t += str(int(interpretation.evaluate(formula)))

        t+="\n"
    return t



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


def TTcarry(n):
    x = [cpl.Proposition(index=i) for i in range(n+1)]
    res = 0
    for i in range(0, n):
        term = x[i]*x[i+1]
        prod = 1
        for j in range(0, math.floor((n-i-3)/2)+1):
            prod = x[2*j+3+i] * prod
        term = term * prod
        res = term + res
    return res


def TTcarry_negated(n):
    x = [cpl.Proposition(index=i) for i in range(n+1)]
    if n == 1:
        return (-x[0]) + (-x[1])
    if n == 2:
        return (-x[1]) + ( (-x[0]) * (-x[2]) )

    term1 = 1
    for k in range(math.floor(n/2)+1):
        term1 = (-x[2*k]) * term1

    term2_part1 = 1
    for k in range(1, math.floor(n/2)+1):
        term2_part1 = (-x[2*k]) * term2_part1

    term2_part2 = 1
    for k in range(1, math.floor((n+1)/2)):
        term2_part2 = (-x[2*k+1]) * term2_part2

    term2 = (-x[1]) * (term2_part1 + term2_part2)

    term3 = 0
    for k in range(2, n):
        tmp = 1
        for l in range(0, math.floor((n-k-3)/2) + 1):
            tmp = (-x[2*l+3+k]) * tmp

        tmp = (-x[k])*(-x[k+1]) * tmp

        term3 = tmp + term3

    return term1 + term2 + term3


# n = number of digits
def TTslow(n):
    if n == 1:
        return [cpl.Proposition(index=0), cpl.Proposition(index=0)]

    if n == 2:
        x0 = cpl.Proposition(index=0)
        x1 = cpl.Proposition(index=1)

        z0 = x0
        z1 = HA_sum(x0, x1)
        z2 = simplify(HA_sum(x1, HA_cout(x0,x1)))
        z3 = simplify(HA_cout(x1, HA_cout(x0,x1)))

        return [z0, z1, z2, z3]

    x = [cpl.Proposition(index=i) for i in range(n)]
    res = [x[0], HA_sum(x[1], x[0])]
    carry = HA_cout(x[1], x[0])

    for i in range(2, len(x)):
        digit = simplify(FA_sum(x[i], x[i-1], carry))
        carry = TTcarry(i)
        res.append(digit)

    res.append(simplify(HA_sum(x[-1], TTcarry(n-1))))
    res.append(simplify(HA_cout(x[-1], TTcarry(n-1))))

    return res


def TT(n):
    """ like TT_slow but faster """
    x = [cpl.Proposition(index=i) for i in range(n)]

    if n == 1:
        return [x[0], x[0]]

    if n == 2:
        x0 = x[0]
        x1 = x[1]

        z0 = x0
        z1 = HA_sum(x0, x1)
        z2 = simplify(HA_sum(x1, HA_cout(x0,x1)))
        z3 = simplify(HA_cout(x1, HA_cout(x0,x1)))

        return [z0, z1, z2, z3]

    term1 = [x[0], HA_sum(x[1], x[0])]
    #term2 = [FA_sum(x[i], x[i-1], TTcarry(i)) for i in range(2,n)] bad
    #TTcarry(n)*( (-x)*(-y) + x*y ) + TTcarry_negated(n)*( (-x)*y + x*(-y) ) bad
    term2 = [TTcarry(i)*( (-x[i]) * (-x[i-1]) ) + TTcarry_negated(i)*( (-x[i])*x[i-1] + x[i]*(-x[i-1]) ) for i in range(2,n)]
    term3 = [HA_sum(x[-1], TTcarry(n-1)), HA_cout(x[-1], TTcarry(n-1))]


    return term1 + term2 + term3


def number_to_interpretation(n, bound):
    q = str(bin(n))[2:][::-1]
    bound_len = len(str(bin(bound))[2:])

    #x = [cpl.Proposition(index=i) for i in range(len(q))]
    x = [cpl.Proposition(index=i) for i in range(bound_len)]
    dict_ = {}

    for i in range(len(q)):
        dict_[x[i]] = (q[i] == "1")

    for j in range(len(q), bound_len):
        dict_[x[j]] = False

    return cpl.Interpretation(dict_)


def interpretation_to_number(interpretation):
    x = sorted(interpretation.keys())
    num = 0
    for i in range(len(x)):
        if interpretation.evaluate(x[i]):
            num += 2 ** i
    return num


def formula_interpretation_to_number(interpretation, formulas):
    num = 0
    #formulas.reverse()
    for i in range(len(formulas)):
        if interpretation.evaluate(formulas[i]):
            num += 2 ** i
    return num


def minterms(formula):
    "retunrs interpretations that evaluate formula to true"
    interpretations = possible_interpretations(*formula.indexes_involved)
    terms = []
    for i in range(len(interpretations)):
        if interpretations[i].evaluate(formula):
            terms.append(i)
            #terms.append(interpretations[i])

    return terms


def onescount(n):
    count = 0
    while n > 0:
        count += 1
        n &= (n-1)
    return count


def robert_to_travis(robert_terms, indexes_involved):
    con = []
    l = len(indexes_involved)-1
    for term in robert_terms:
        tmp = []
        for i in range(len(term)-1,-1,-1):
            if term[i] == "X":
                continue
            if term[i] == "1":
                tmp.append(cpl.Proposition(index=indexes_involved[l-i]).to_literal())
            else:
                tmp.append(-(cpl.Proposition(index=indexes_involved[l-i])))
        if tmp:
            con.append(cpl.Conjunction(*tmp))
        #print(tmp)
    new_formula = cpl.DNF(*con)
    return new_formula


#QuineMcClouskey
def simplify(formula):
    ones = minterms(formula)
    rober_terms = qm.qm(ones=ones)
    newfor = robert_to_travis(rober_terms, formula.indexes_involved)
    return newfor


def asmatrix(formula):
    """ only works for DNF """
    mat = []
    for conjunction in formula.conjunctions:
        row = []

        for i in range(max(formula.indexes_involved)+1):
            for literal in conjunction.literals:
                skip = False
                if literal.indexes_involved[0] == i:
                    if literal.negated:
                        row.append(-1)
                    else:
                        row.append(1)
                    skip = True
                    break
            if skip:
                continue
            else:
                row.append(0)
        mat.append(row)

    return mat

def pretty_matrix(mat):
    tmp = ""
    for row in mat:
        for el in row:
            if el == -1:
                tmp += "-1 "
            elif el == 1:
                tmp += " 1 "
            elif el == 0:
                tmp += " 0 "
        tmp += "\n"
    return tmp


def split_matrix(mat):
    ones = deepcopy(mat)
    minus_ones = deepcopy(mat)

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if minus_ones[i][j] == 1: minus_ones[i][j] = 0
            if ones[i][j] == -1: ones[i][j] = 0

    return minus_ones, ones


def count_propositions(formula):
    dic = {}
    for index in formula.indexes_involved:
        dic[index] = 0
    for conjunction in formula.conjunctions:
        for literal in conjunction.literals:
            dic[literal.indexes_involved[0]] += 1

    return dic


def len_binary_digits(num):
    return len(str(bin(num))[2:])


def fast_FA_sum(x, y, n):
    return TTcarry(n)*( (-x)*(-y) + x*y ) + TTcarry_negated(n)*( (-x)*y + x*(-y) )
