import cpl
import functions as fun
import qm

def carry(x,i):
    if i == 0 or i >= len(x):
        return -1

    if i == 1:
        return fun.HA_cout(x[1],x[0])

    return fun.FA_cout(x[i], x[i-1], carry(x, i-1))

n = 7

x = [cpl.Proposition() for i in range(n+1)]

actual = carry(x,n)

terms = fun.minterms(actual)
res = qm.qm(ones=terms)

print(n)
print(fun.robert_to_travis(res,[i for i in range(n+1)]))
