from .token import Token
from core import Grammar
from core import non_recursive_descending_parser_fixed, evaluate_left_parse
from .ast import UnionNode, ConcatNode, SymbolNode, EpsilonNode, ClosureNode
from .automaton.utils import nfa_to_dfa

def build_grammar():
    G = Grammar()

    E = G.add_non_terminal('E', True)
    T, F, A, X, Y, Z = G.add_non_terminals('T F A X Y Z')
    pipe, star, opar, cpar, symbol, epsilon = G.add_terminals('| ^ { } symbol ε')

    E %= T + X, lambda h, s: s[2], None, lambda h,s: s[1]

    T %= F + Y,lambda h, s: s[2], None, lambda h, s: s[1]

    X %= pipe + T + X, lambda h,s: s[3] , None, None, lambda h, s: UnionNode(h[0], s[2])
    X %= G.epsilon, lambda h, s: h[0]

    F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]

    Y %= F + Y, lambda h, s: s[2], None, lambda h, s: ConcatNode(h[0], s[1])
    Y %= G.epsilon, lambda h, s: h[0]

    A %= symbol, lambda h, s: SymbolNode(s[1]), None
    A %= opar + E + cpar, lambda h, s: s[2], None, None, None
    A %= epsilon, lambda h, s: EpsilonNode(s[1]), None

    Z %= star + Z, lambda h, s: s[2], None, lambda h, s: ClosureNode(h[0])
    Z %= G.epsilon, lambda h, s: h[0]

    return G

class Regex:
    def __init__(self, regex, skip_spaces = False):
        self.regex = regex
        self.automaton = self.build_automaton(regex, skip_spaces)

    def regex_tokenizer(self, text, G, skip_spaces):
        tokens = []
        regex_tokens = {symbol: Token(symbol, G[symbol]) for symbol in ['|', '^', '{', '}', 'ε']}
        for c in text:
            if(c == " " and skip_spaces):
                continue
            if(regex_tokens.__contains__(c)):
                tokens.append(regex_tokens[c])
            else:
                tokens.append(Token(c, G['symbol']))

        tokens.append(Token('$', G.eof))
        return tokens

    def build_automaton(self, regex, skip_spaces):
        G = build_grammar()
        tokens = self.regex_tokenizer(regex, G, skip_spaces)
        parser = non_recursive_descending_parser_fixed(G)
        left_parse = parser(tokens)
        ast = evaluate_left_parse(left_parse, tokens)
        automaton = ast.evaluate()
        dfa = nfa_to_dfa(automaton)
        return dfa
