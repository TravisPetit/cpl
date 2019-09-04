import cpl
import functions as fun
import qm
import math


#Currently NOT woking for 7!!!!!!!!! probably because 7 is a 3 bit number

for i in range(9):
    digits = fun.len_binary_digits(i)

    #inter = fun.number_to_interpretation(i, fun.len_binary_digits(i*3))
    inter = fun.number_to_interpretation(i, 100)

    t3 = fun.TT(digits)
    #t3 = fun.TTslow(digits)

    result = fun.formula_interpretation_to_number(inter, t3)

    print(result)

    #if i == 0:
    #    continue
    #ori = fun.TTcarry(i)
    #neg = fun.TTcarry_negated(i)

    #for interpretation in fun.possible_interpretations(*[a for a in range(i+1)]):
    #    if (interpretation.evaluate(ori) == interpretation.evaluate(neg)):
    #        print("bad")
