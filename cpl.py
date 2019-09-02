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

        self.__indexes_involved = (self.__indx,)

    def __repr__(self):
        return "x{}".format(str(self.__indx).translate(Proposition.SUB))

    @property
    def index(self):
        return self.__indx

    @property
    def indexes_involved(self):
        return self.__indexes_involved

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

    def __add__(self, other):
        return self.to_literal(negated=False) + other

    def __mul__(self, other):
        return self.to_literal(negated=False) * other

    def __neg__(self):
        return self.to_literal(negated=True)

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

    @property
    def indexes_involved(self):
        return self.proposition.indexes_involved

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
        if isinstance(other, int):
            if other == 1:
                return self
        if isinstance(other, Literal):
            return Conjunction(self, other)

        if isinstance(other, Conjunction):
            c = list(other.literals)
            c.append(self)
            return Conjunction(*c)

        if isinstance(other, Proposition):
            return Conjunction(self, Literal(other, negated=False))

        if isinstance(other, DNF):
            return other * self

        #if isinstance(other, Conjunction):
        #    return other * self

        raise MulException(self, other)

    def __neg__(self):
        return Literal(self.__proposition, not self.__negated)

    def __add__(self, other):
        if isinstance(other, int):
            if other == 0:
                return self
        if isinstance(other, Literal):
            return Conjunction(self) + Conjunction(other)

        if isinstance(other, Proposition):
            return Conjunction(self) + Conjunction(other.to_literal())

        if isinstance(other, Conjunction) or isinstance(other, DNF):
            return other + self

        raise Exception("TODO")


class Conjunction:

    def __init__(self, *literals):
        self.__literals = list(literals)
        self.__literals.sort()
        self.__literals = tuple(self.__literals)

        self.__indexes_involved = set(literal.proposition.index for literal in self.__literals)
        self.__indexes_involved = list(self.__indexes_involved)
        self.__indexes_involved.sort()
        self.__indexes_involved = tuple(self.__indexes_involved)

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

    @property
    def indexes_involved(self):
        return self.__indexes_involved

    def __eq__(self, other):
        return self.__literals == other.literals

    def __mul__(self, other):
        if isinstance(other, int):
            if other == 1:
                return self
        if isinstance(other, Literal):
            l = list(self.__literals)
            l.append(other)
            return Conjunction(*l)

        if isinstance(other, Proposition):
            lit = other.to_literal(negated=False)
            return self * lit

        if isinstance(other, Conjunction):
            s = list(other.__literals) + list(self.__literals)
            return Conjunction(*s)

        if isinstance(other, DNF):
            return other * self

        raise MulException(self, other)

    def __add__(self, other):
        if isinstance(other, int):
            if other == 0:
                return self
        if isinstance(other, Proposition):
            return self + Conjunction(other.to_literal())

        if isinstance(other, Conjunction):
            return DNF(self, other)

        if isinstance(other, DNF):
            l = list(other.conjunctions)
            l.append(self)
            return DNF(*l)

        if isinstance(other, Literal):
            return self + Conjunction(other)

        raise Exception("TODO: conjuntion + {}".format(type(other)))


    def __hash__(self):
        return hash(self.__literals)


    def __neg__(self):

        if len(self.__literals) == 0:
            raise Exception("Empty conjunction")

        if len(self.__literals) == 1:
            return (-self.__literals[0])

        c = (-self.__literals[0])
        for i in range(1, len(self.__literals)):
            c = c + (-self.__literals[i])

        return c


class DNF:

    def __init__(self, *conjunctions):
        self.__conjunctions = list(conjunctions)
        self.__conjunctions.sort()
        self.__conjunctions = tuple(self.__conjunctions)

        self.__indexes_involved = set()
        for conjunction in self.__conjunctions:
            self.__indexes_involved = self.__indexes_involved.union(set(conjunction.indexes_involved))
        self.__indexes_involved = list(self.__indexes_involved)
        self.__indexes_involved.sort()
        self.__indexes_involved = tuple(self.__indexes_involved)

    @property
    def conjunctions(self):
        return self.__conjunctions

    @property
    def indexes_involved(self):
        return self.__indexes_involved

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

    def __neg__(self):
        list_ = [-con for con in self.__conjunctions]
        x = list_[0]
        for i in range(1, len(list_)):
            x = x * list_[i]
        return x

    def __eq__(self, other):
        return self.__conjunctions == other.conjunctions


    def __lt__(self, other):
        if len(self.__conjunctions) < other.conjunctions:
            return True

        if len(self.__conjunctions) > other.conjunctions:
            return False

        for i in range(self.__conjunctions):
            if self.__conjunctions[i] == other.conjunctions[i]:
                continue

            return self.__conjunctions[i] < other.conjunctions[i]

    def __gt__(self, other):
        return not self.__lt__(self, other)

    def __add__(self, other):

        if isinstance(other, int):
            if other == 0:
                return self

        if isinstance(other, DNF):
            c = set(self.__conjunctions).union(set(other.conjunctions))
            c = list(c)
            return DNF(*c)

        if isinstance(other, Literal):
            con = Conjunction(other)
            c = list(self.__conjunctions)
            c.append(con)
            return DNF(*c)

        if isinstance(other, Proposition):
            return self + other.to_literal()

        if isinstance(other, Conjunction):
            return other + self

        raise Exception("TODO DNF {} {}".format(type(other), other))


    def __mul__(self, other):

        if isinstance(other, int):
            if other == 1:
                return self

        if isinstance(other, Literal) or isinstance(other, Proposition) or isinstance(other, Conjunction):
            list_ = []
            for conjunction in self.__conjunctions:
                list_.append(conjunction * other)
            return DNF(*list_)

        if isinstance(other, DNF):
            list_ = []
            for my_conjunction in self.__conjunctions:
                for your_conjunction in other.__conjunctions:
                    list_.append(my_conjunction * your_conjunction)

            return DNF(*list_)

        #if isinstance(other, Conjunction):
        #    list_ = []
        #    for literals in other.__literals:
        #        list_.append(self * literal)


        raise MulException(self, other)




class Interpretation(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable

    def evaluate(self, obj):
        if isinstance(obj, Proposition):
            return self[obj]

        if isinstance(obj, Literal):
            if obj.negated:
                return not self[obj.proposition]
            return self[obj.proposition]

        if isinstance(obj, Conjunction):
            for literal in obj.literals:
                if not self.evaluate(literal):
                    return False
            return True

        if isinstance(obj, DNF):
            for conjunction in obj.conjunctions:
                if self.evaluate(conjunction):
                    return True
            return False

        raise Exception("Bad input") #TODO

    def __repr__(self):
        s = "\n"
        for item in sorted(self.items()):
            prop = item[0]
            val = item[1]
            s += "{} -> {}\n".format(prop, int(val))
        #return "\n" + s.strip()
        return s
