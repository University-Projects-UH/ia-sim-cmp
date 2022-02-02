from core import Grammar, Sentence, Production
from core import compute_firsts, compute_follows
from core import descending_not_recursive_parser, build_table_parser_ll1, is_ll1
from core import ContainerSet

def test_answer():

    class ExampleGrammar:
        def __init__(self, G):
            self.G = G

        @property
        def firsts(self):
            G = self.G
            return {
                G['+']: ContainerSet(G['+'] , contains_epsilon=False),
                G['-']: ContainerSet(G['-'] , contains_epsilon=False),
                G['*']: ContainerSet(G['*'] , contains_epsilon=False),
                G['/']: ContainerSet(G['/'] , contains_epsilon=False),
                G['(']: ContainerSet(G['('] , contains_epsilon=False),
                G[')']: ContainerSet(G[')'] , contains_epsilon=False),
                G['num']: ContainerSet(G['num'] , contains_epsilon=False),
                G['E']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
                G['T']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
                G['F']: ContainerSet(G['num'], G['('] , contains_epsilon=False),
                G['X']: ContainerSet(G['-'], G['+'] , contains_epsilon=True),
                G['Y']: ContainerSet(G['/'], G['*'] , contains_epsilon=True),
                Sentence(G['T'], G['X']): ContainerSet(G['num'], G['('] , contains_epsilon=False),
                Sentence(G['+'], G['T'], G['X']): ContainerSet(G['+'] , contains_epsilon=False),
                Sentence(G['-'], G['T'], G['X']): ContainerSet(G['-'] , contains_epsilon=False),
                G.epsilon: ContainerSet( contains_epsilon=True),
                Sentence(G['F'], G['Y']): ContainerSet(G['num'], G['('] , contains_epsilon=False),
                Sentence(G['*'], G['F'], G['Y']): ContainerSet(G['*'] , contains_epsilon=False),
                Sentence(G['/'], G['F'], G['Y']): ContainerSet(G['/'] , contains_epsilon=False),
                Sentence(G['num']): ContainerSet(G['num'] , contains_epsilon=False),
                Sentence(G['('], G['E'], G[')']): ContainerSet(G['('] , contains_epsilon=False)
            }

        @property
        def follows(self):
            G = self.G
            return {
                G['E']: ContainerSet(G[')'], G.eof , contains_epsilon=False),
                G['T']: ContainerSet(G[')'], G['-'], G.eof, G['+'] , contains_epsilon=False),
                G['F']: ContainerSet(G['-'], G.eof, G['*'], G['/'], G[')'], G['+'] , contains_epsilon=False),
                G['X']: ContainerSet(G[')'], G.eof , contains_epsilon=False),
                G['Y']: ContainerSet(G[')'], G['-'], G.eof, G['+'] , contains_epsilon=False)
            }

        @property
        def table(self):
            G = self.G
            return {
                ( G['E'], G['num'], ): [ Production(G['E'], Sentence(G['T'], G['X'])) ],
                ( G['E'], G['('], ): [ Production(G['E'], Sentence(G['T'], G['X'])) ],
                ( G['X'], G['+'], ): [ Production(G['X'], Sentence(G['+'], G['T'], G['X'])) ],
                ( G['X'], G['-'], ): [ Production(G['X'], Sentence(G['-'], G['T'], G['X'])) ],
                ( G['X'], G[')'], ): [ Production(G['X'], G.epsilon) ],
                ( G['X'], G.eof, ): [ Production(G['X'], G.epsilon) ],
                ( G['T'], G['num'], ): [ Production(G['T'], Sentence(G['F'], G['Y'])) ],
                ( G['T'], G['('], ): [ Production(G['T'], Sentence(G['F'], G['Y'])) ],
                ( G['Y'], G['*'], ): [ Production(G['Y'], Sentence(G['*'], G['F'], G['Y'])) ],
                ( G['Y'], G['/'], ): [ Production(G['Y'], Sentence(G['/'], G['F'], G['Y'])) ],
                ( G['Y'], G[')'], ): [ Production(G['Y'], G.epsilon) ],
                ( G['Y'], G['-'], ): [ Production(G['Y'], G.epsilon) ],
                ( G['Y'], G.eof, ): [ Production(G['Y'], G.epsilon) ],
                ( G['Y'], G['+'], ): [ Production(G['Y'], G.epsilon) ],
                ( G['F'], G['num'], ): [ Production(G['F'], Sentence(G['num'])) ],
                ( G['F'], G['('], ): [ Production(G['F'], Sentence(G['('], G['E'], G[')'])) ]
            }

    G = Grammar()
    E = G.add_non_terminal('E', True)
    T,F,X,Y = G.add_non_terminals('T F X Y')
    plus, minus, star, div, opar, cpar, num = G.add_terminals('+ - * / ( ) num')

    E %= T + X
    X %= plus + T + X | minus + T + X | G.epsilon
    T %= F + Y
    Y %= star + F + Y | div + F + Y | G.epsilon
    F %= num | opar + E + cpar

    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
    table = build_table_parser_ll1(G, firsts, follows)

    parser = descending_not_recursive_parser(G, table)
    left_parse = parser([num, star, opar, num, plus, num, cpar, G.eof])

    true_parse = [
        Production(E, Sentence(T, X)),
        Production(T, Sentence(F, Y)),
        Production(F, Sentence(num)),
        Production(Y, Sentence(star, F, Y)),
        Production(F, Sentence(opar, E, cpar)),
        Production(E, Sentence(T, X)),
        Production(T, Sentence(F, Y)),
        Production(F, Sentence(num)),
        Production(Y, G.epsilon),
        Production(X, Sentence(plus, T, X)),
        Production(T, Sentence(F, Y)),
        Production(F, Sentence(num)),
        Production(Y, G.epsilon),
        Production(X, G.epsilon),
        Production(Y, G.epsilon),
        Production(X, G.epsilon)
    ]

    grammar = ExampleGrammar(G)
    assert firsts == grammar.firsts
    assert follows == grammar.follows
    assert table == grammar.table
    assert left_parse == true_parse
    assert is_ll1(G, table) == True