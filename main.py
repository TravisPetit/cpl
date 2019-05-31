import cpl
import functions as fun
import qm
import math

def guess(n):
    x = [cpl.Proposition(index=i) for i in range(n+1)]
    q = lambda i : int(i+1 < n)
    res = 0
    for i in range(0, int(math.ceil(n))):
        for j in range(0, q(i)+1):
            res = x[2*i+j]*x[2*i+j+1] + res
            for k in range(0,n-j-3-i+1):
                if k > n-j-3-i:
                    continue
                res = x[2*k+j+3] * res
    return res


def carry(x,i):
    if i == 0 or i >= len(x):
        return -1

    if i == 1:
        return fun.simplify(fun.HA_cout(x[1],x[0]))

    return fun.simplify(fun.FA_cout(x[i], x[i-1], carry(x, i-1)))

n = 2

x = [cpl.Proposition() for i in range(n+1)]

actual = carry(x,n)
g = guess(n)

print(n)
print(actual)
print(g)
