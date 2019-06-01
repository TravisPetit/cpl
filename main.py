import cpl
import functions as fun
import qm
import math

def guess(n):
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


def carry(x,i):
    if i == 0 or i >= len(x):
        return -1

    if i == 1:
        return fun.simplify(fun.HA_cout(x[1],x[0]))

    return fun.simplify(fun.FA_cout(x[i], x[i-1], carry(x, i-1)))

n = 9

x = [cpl.Proposition() for i in range(n+1)]

actual = carry(x,n)
g = guess(n)

print(n)
print("actual")
print(actual)
print("guess")
print(g)
