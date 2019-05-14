class MulException(Exception):
    def __init__(self, multiplicand, multiplier):
        s_multiplicand = str(type(multiplicand)).replace("<class","").replace(">","")
        s_multiplier = str(type(multiplier)).replace("<class","").replace(">","")
        self.__message = "\nCannot multiply  {}  and  {}\nnamely: {} * {}".format(s_multiplicand, s_multiplier, multiplicand, multiplier)

    def __str__(self):
        return self.__message


class Proposition:
    class_indx = 0
    SUB = str.maketrans("0123456789", "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089")

    def __init__(self, index=None):
        if index is not None:
            self.__indx = index
        else:
            self.__indx = Proposition.class_indx
            Proposition.class_indx += 1

    def __repr__(self):
        return "x{}".format(str(self.__indx).translate(Proposition.SUB))

    @property
    def index(self):
        return self.__indx

    def __eq__(self, other):
        return self.__indx == other.index

    def __lt__(self, other):
        return self.__indx < other.index

    def __gt__(self, other):
        return self.__indx > other.index

    def __hash__(self):
        return hash(self.__indx)

    def to_literal(self, negated=False):
        return Literal(self, negated)

    def __mul__(self, other):
        return self.to_literal(negated=False) * other

    @staticmethod
    def reset():
        Proposition.class_indx = 0


class Literal:

    def __init__(self, prop, negated=False):
        self.__proposition = prop
        self.__negated = negated

    @property
    def proposition(self):
        return self.__proposition

    @property
    def negated(self):
        return self.__negated

    def __eq__(self, other):
        return self.__proposition == other.proposition and self.__negated == other.negated

    def __lt__(self, other):
        if self.__proposition == other.proposition:
            return self.negated

        return self.__proposition < other.proposition

    def __gt__(self, other):
        if self.__proposition == other.proposition:
            return not self.__negated

        return self.__proposition > other.proposition

    def __repr__(self):
        if self.__negated:
            return str(self.__proposition).capitalize()
        return str(self.__proposition)

    def __hash__(self):
        return hash( (self.__proposition, self.__negated) )

    def __mul__(self, other):
        if isinstance(other, Literal):
            return Conjunction(self, other)

        if isinstance(other, Conjunction):
            c = list(other.literals)
            c.append(self)
            return Conjunction(*c)

        if isinstance(other, Proposition):
            return Conjunction(self, Literal(other, negated=False))

        if isinstance(other, Conjunction):
            return other * self

        raise MulException(self, other)


class Conjunction:

    def __init__(self, *literals):
        self.__literals = list(literals)
        self.__literals.sort()
        self.__literals = tuple(self.__literals)

    def __repr__(self):
        s = ""
        for literal in self.__literals:
            s += str(literal)
        return s

    def __lt__(self, other):
        if len(self.__literals) < len(other.literals):
            return True

        if len(self.__literals) > len(other.literals):
            return False

        for i in range(len(self.__literals)):
            if self.__literals[i] == other.literals[i]:
                continue
            return self.__literals[i] < other.literals[i]


    def __gt__(self, other):
        return not self.__lt__(self, other)

    @property
    def literals(self):
        return self.__literals

    def __eq__(self, other):
        return self.__literals == other.literals

    def __mul__(self, other):
        if isinstance(other, Literal):
            l = list(self.__literals)
            l.append(other)
            return Conjunction(*l)

        if isinstance(other, Proposition):
            lit = other.to_literal(negated=False)
            return self * lit

        raise MulException(self, other)

    def __hash__(self):
        return hash(self.__literals)

class DNF:

    def __init__(self, *conjunctions):
        self.__conjunctions = list(conjunctions)
        self.__conjunctions.sort()
        self.__conjunctions = tuple(self.__conjunctions)

    @property
    def conjunctions(self):
        return self.__conjunctions

    def __str__(self):
        s = ""
        for i in range(len(self.__conjunctions)):
            if i == len(self.__conjunctions) - 1:
                s += str(self.__conjunctions[i])
            else:
                s += "{} + ".format(str(self.__conjunctions[i]))
        return s

    def __hash__(self):
        return hash(self.__conjunctions)



class Valuation:

    def __init__(self, dict_):
        self.__dict_ = dict_

    def evaluate(obj):
        if isinstance(obj, Proposition):
            if obj not in self.__dict_:
                raise Exception("the proposition is not defined")
            return self.__dict_[obj]
