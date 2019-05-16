import unittest
import cpl
import functions as fun

class TestCPL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        num = 20
        global propositions, literals
        propositions = [cpl.Proposition() for i in range(num)]
        literals = [cpl.Literal(propositions[i], bool(i%2)) for i in range(num)]

    def test_propositions_index(self):
        for i in range(len(propositions)):
            self.assertEqual(propositions[i].index,i)

    def test_propositions_equality(self):
        for i in range(len(propositions)):
            for j in range(len(propositions)):
                if i == j:
                    self.assertEqual(propositions[i], propositions[j])
                else:
                    self.assertNotEqual(propositions[i], propositions[j])

    def test_propositions_cp(self):
        for i in range(len(propositions)-1):
            for j in range(i+1, len(propositions)):
                self.assertLess(propositions[i], propositions[j])
                self.assertGreater(propositions[j], propositions[i])


    def test_propositions_hash(self):
        propositions_copy = propositions.copy()
        for i in range(len(propositions)):
            self.assertEqual(hash(propositions[i]), hash(propositions_copy[i]))


    def test_literals_equality(self):
        for i in range(len(literals)):
            self.assertNotEqual(literals[i], cpl.Literal(propositions[i], not literals[i].negated))
            for j in range(len(literals)):
                if i == j:
                    self.assertEqual(literals[i], literals[j])
                else:
                    self.assertNotEqual(literals[i], literals[j])

    def test_literals_cp(self):
        for i in range(len(literals)):
            if literals[i].negated:
                self.assertLess(literals[i], cpl.Literal(propositions[i], False))
                self.assertGreater(cpl.Literal(propositions[i], False), literals[i])
            else:
                self.assertLess(cpl.Literal(propositions[i], True), literals[i])
                self.assertGreater(literals[i], cpl.Literal(propositions[i], True))

            for j in range(i+1, len(literals)):
                self.assertLess(literals[i], literals[j])
                self.assertLess(literals[i], cpl.Literal(propositions[j], not literals[j].negated))

                self.assertGreater(literals[j], literals[i])
                self.assertGreater(cpl.Literal(propositions[j], not literals[j].negated), literals[i])


    def test_conjuntions(self):
        for i in range(len(literals)):
            for j in range(len(literals)):

                self.assertEqual(literals[i] * literals[j], literals[j] * literals[i])
                self.assertEqual(hash(literals[i] * literals[j]), hash(literals[j] * literals[i]))

                for k in range(len(literals)):
                    p1 = literals[i] * literals[j] * literals[k]
                    p2 = literals[k] * literals[i] * literals[j]

                    self.assertEqual(p1, p2)
                    self.assertEqual(hash(p1), hash(p2))

                    assignemnts = fun.possible_interpretations(i,j,k)
                    for assignemnt in assignemnts:
                        self.assertEqual(assignemnt.evaluate(p1), assignemnt.evaluate(p2))


    def test_DNF(self):
        for i in range(len(literals)):
            for j in range(len(literals)):
                for k in range(len(literals)):
                    li = literals[i]
                    lj = literals[k]
                    lk = literals[j]
                    dnf1 = (li*lj*lk) + (li*lk) + li
                    dnf2 = (lk*li) + li + (lj*lk*li)
                    self.assertEqual(dnf1, dnf2)
                    self.assertEqual(hash(dnf1), hash(dnf2))

                    assignemnts = fun.possible_interpretations(i,j,k)
                    for assignemnt in assignemnts:
                        self.assertEqual(assignemnt.evaluate(dnf1), assignemnt.evaluate(dnf2))


    def test_DNF_eq(self):
        for i in range(10):
            x = fun.random_formula()
            y = fun.random_formula()
            xpy = x + y
            xty = x * y
            l = [i for i in range(max(xty.indexes_involved[-1], xpy.indexes_involved[-1])+1)]

            for interpretation in fun.possible_interpretations(*l):
                ix = interpretation.evaluate(x)
                iy = interpretation.evaluate(y)
                self.assertEqual(ix or iy, interpretation.evaluate(xpy))
                self.assertEqual(ix and iy, interpretation.evaluate(xty))


    def test_DNF_neg(self):
        for i in range(10):
            x = fun.random_formula()
            mx = -x
            l = [i for i in range(x.indexes_involved[-1]+1)]
            for interpretation in fun.possible_interpretations(*l):
                self.assertEqual(interpretation.evaluate(x), not interpretation.evaluate(mx))



if __name__ == '__main__':
    unittest.main()
