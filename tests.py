import unittest
import cpl

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




if __name__ == '__main__':
    unittest.main()