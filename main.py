import cpl

x0 = cpl.Proposition()
x1 = cpl.Proposition()

y = cpl.Literal(x0, negated=False)
z = cpl.Literal(x1, negated=True)

c1 = x0*x1*x0
c1 = c1 * x0

print(c1)
