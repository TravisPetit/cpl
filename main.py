import cpl
import functions as fun
import qm
import math


# not working
def guess(n):
    x = [cpl.Proposition(index=i) for i in range(n+1)]

    res = 0
    for k in range(n-1):
        term1 = x[k]*x[k+1]
        term2 = 1
        for l in range(math.floor((n-k-5)/2)-k+1): #+1 porque el ultimo no cuenta
            term2 = x[2*l+k] * term2
        term3 = x[n-1] * ((-1) ** (n-k)) * x[n] * ((-1) ** (n-k))
        intermediate = term1 * term2 * term3
        res = intermediate + res

    return res


n = 10
x = [cpl.Proposition(index=i) for i in range(n)]

for i in range(2, n):
    formula = fun.TERM1(x[i], x[i-1], fun.TTcarry(i-1))
    sf = fun.simplify(formula)
    #print(formula)
    print(i)
    print(sf)
    print(guess(i))
    print("----------")
