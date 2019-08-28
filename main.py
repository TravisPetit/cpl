import cpl
import functions as fun
import qm
import math

#def guess(n):
#    x = [cpl.Proposition(index=i) for i in range(n+1)]
#    res = 0
#    for i in range(0, n):
#        term = x[i]*x[i+1]
#        prod = 1
#        for j in range(0, math.floor((n-i-3)/2)+1):
#            prod = x[2*j+3+i] * prod
#        term = term * prod
#        res = term + res
#    return res
#
#
#def carry(x,i):
#    if i == 0 or i >= len(x):
#        return -1
#
#    if i == 1:
#        return fun.simplify(fun.HA_cout(x[1],x[0]))
#
#    return fun.simplify(fun.FA_cout(x[i], x[i-1], carry(x, i-1)))
#
#n = 9
#
#x = [cpl.Proposition() for i in range(n+1)]
#
#actual = carry(x,n)
#g = guess(n)
#
#print(n)
#print("actual")
#print(actual)
#print("guess")
#print(g)


#n = 7
#bound = n + 100
#inter = fun.number_to_interpretation(n, bound)
#print(fun.formula_interpretation_to_number(inter, fun.TT(n)))



#for n in range(1, 8):
#    bound = 100
#    inter = fun.number_to_interpretation(n, 100)
#    print(fun.formula_interpretation_to_number(inter, fun.TT(n)))


n = 6
for i in range(1,n+1):
    x = [cpl.Proposition(index=k) for k in range(i+1)]
    formula = fun.FA_sum(x[i], x[i-1], fun.TTcarry(i))
    formula = fun.simplify(formula)
    print(i)
    print(formula)
    print(fun.pretty_matrix(fun.asmatrix(formula)))
    print("--")



#x = [cpl.Proposition(index=i) for i in range(11)]
#
#test = cpl.DNF(x[0]*x[1], (-x[0])*x[2])
#test2 = (x[10]*x[1]) + ((-x[0])*x[2])
#print(test)
##print(test2)
#
#mat = fun.asmatrix(test)
#print(mat)
#print(fun.pretty_matrix(mat))
