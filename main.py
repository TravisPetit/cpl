import cpl
import functions as fun
import qm
import math


#Currently NOT woking for 7!!!!!!!!! probably because 7 is a 3 bit number
for i in range(8):
    digits = fun.len_binary_digits(i)

    inter = fun.number_to_interpretation(i, fun.len_binary_digits(i*3))

    t3 = fun.TT(digits)

    result = fun.formula_interpretation_to_number(inter, t3)

    print(result)
