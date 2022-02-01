
from firsts_follows import compute_firsts


class Symbol:
    
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, elem):

        if isinstance(elem, Symbol):
            return Sentence(self, elem)

        raise TypeError(elem)

    def __or__(self, elem):

        if isinstance(elem, (Sentence)):
            return SentenceList(Sentence(self), elem)

        raise TypeError(elem)

    @property
    def is_epsilon(self):
        return False

    def __len__(self):
        return 1


class NonTerminal(Symbol):

    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        self.productions = []

    def __imod__(self, elem):

        if isinstance(elem, (Sentence)):

            p = Production(self, elem)
            self.grammar.add_production(p)
            return self

        if isinstance(elem, Symbol):

            p = Production(self, Sentence(elem))
            self.grammar.add_production(p)
            return self

        if isinstance(elem, SentenceList):

            for sentence in elem:

                p = Production(self, sentence)
                self.grammar.add_production(p)

            return self

        raise TypeError(elem)

    @property
    def is_terminal(self):
        return False

    @property
    def is_nonTerminal(self):
        return True

    @property
    def is_epsilon(self):
        return False


class Terminal(Symbol):

    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        
    @property
    def is_terminal(self):
        return True

    @property
    def is_nonTerminal(self):
        return False


class Sentence:

    def __init__(self, *args):
        self.symbols = tuple(s for s in args if not s.is_epsilon)

    def __add__(self, elem):

        if isinstance(elem, Symbol):
            return Sentence(*(self.symbols + (elem,)))

        if isinstance(elem, Sentence):
            return Sentence(*(self.symbols + elem.symbols))

        raise TypeError(elem)

    def __or__(self, elem):

        if isinstance(elem, Sentence):
            return SentenceList(self, elem)

        if isinstance(elem, Symbol):
            return SentenceList(self, Sentence(elem))

        TypeError(elem)

    def __str__(self):
        return ("%s " * len(self.symbols) % tuple(self.symbols)).strip()

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.symbols)

    def __len__(self):
        return len(self.symbols)

    @property
    def is_epsilon(self):
        return False

class SentenceList:

    def __init__(self, *args):
        self.sentences = list(args)

    def add(self, symbol):

        if not symbol and (symbol is None or not symbol.is_epsilon):
            raise ValueError(symbol)

        self.sentences.append(symbol)

    def __or__(self, elem):

        if isinstance(elem, Sentence):
            self.add(elem)
            return self

        if isinstance(elem, Symbol):
            return self | Sentence(elem)

        raise TypeError(elem)

    def __iter__(self):
        return iter(self.sentences)

class Production:

    def __init__(self, non_terminal, sentence) -> None:
        self.left = non_terminal
        self.right = sentence

    def __str__(self) -> str:
        return "%s := %s" % (self.left, self.right)

    def __repr__(self) -> str:
        return "%s -> %s" % (self.left, self.right)

    @property
    def is_epsilon(self):
        return self.right.is_epsilon


class Epsilon(Terminal, Sentence):

    def __init__(self, grammar):
        super().__init__("eps", grammar)

    def __str__(self):
        return "eps"

    def __repr__(self) -> str:
        return "epsilon"

    def __len__(self):
        return 0

    def __add__(self, elem):
        return elem

    @property
    def is_epsilon(self):
        return True


class EOF(Symbol):

    def __init__(self, grammar):
        super().__init__("$", grammar)


class Grammar:

    def __init__(self):

        self.terminals = []
        self.non_terminals = []
        self.productions = []
        self.start_non_terminal = None
        self.epsilon = Epsilon(self)
        self.eof = EOF(self)

    def add_non_terminal(self, name, start_non_terminal = False):

        name = name.strip()
        if not name:
            raise Exception("Empty name")

        nt = NonTerminal(name, self)

        if start_non_terminal:

            if self.start_non_terminal is None:
                self.start_non_terminal = start_non_terminal
            
            else:
                raise Exception("Connat define more than one start non terminal")

        self.non_terminals.append(nt)
        return nt

    def add_non_terminals(self, names):

        nts = tuple((self.add_non_terminal(nt) for nt in names.strip().split()))
        return nts

    def add_terminal(self, name):

        name = name.strip()

        if not name:
            raise Exception("Empty name")

        t = Terminal(name, self)
        self.terminals.append(t)
        return t

    def add_terminals(self, names):

        ts = tuple((self.add_terminal(t) for t in names.strip().split()))
        return ts

    def add_production(self, production):

        production.left.productions.append(production)
        self.productions.append(production)
    
    def __str__(self):

        ans = "Non Terminals:\n"

        for nt in self.non_terminals:
            ans += "\t"
            ans += str(nt)

        ans += "\n\nTerminals:\n"

        for t in self.terminals:
            ans += "\t"
            ans += str(t)

        ans += "\n\nProductions:\n"

        for p in self.productions:
            ans += repr(p)
            ans += '\n'

        return ans

### Testing the classes implemented above and the compute_firsts algorithm

# G = Grammar()
# E = G.add_non_terminal('E', True)
# T,F,X,Y = G.add_non_terminals('T F X Y')
# plus, minus, star, div, opar, cpar, num = G.add_terminals('+ - * / ( ) num')

# E %= T + X
# X %= plus + T + X | minus + T + X | G.epsilon
# T %= F + Y
# Y %= star + F + Y | div + F + Y | G.epsilon
# F %= num | opar + E + cpar

# print(G)

# firsts = compute_firsts(G)

# for term in firsts:
#     s = "" + str(term) + " : " + str(firsts[term]) 
#     print(s)