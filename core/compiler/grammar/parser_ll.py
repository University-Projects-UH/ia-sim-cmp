from .firsts_follows import compute_firsts, compute_follows

##################################################################

# Rules:

# 1- If X -> W, t in Terminals and t in First(W)    =>    T[X, t] = X -> W
# 2- If X -> W, t in terminals, epsilon in First(W) and t in Follow(X)   =>    T[X, t] = X -> W

##################################################################

def build_table_parser_ll1(G, firsts, follows):

    T = {}

    for production in G.productions:

        X = production.left
        W = production.right

        # Rule 1
        for t in firsts[W]:

            try:
                T[X, t].append(production)
            except KeyError:
                T[X, t] = [production]

        # Rule 2
        if firsts[W].contains_epsilon:

            for t in follows[X]:
                try:
                    T[X, t].append(production)
                except:
                    T[X, t] = [production]

    return T

def is_ll1(G, T = None):

    if not T:

        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        T = build_table_parser_ll1(G, firsts, follows)

    for cell in T:

        # Ambiguous grammar
        if len(T[cell]) > 1:
            return False

    return True

def non_recursive_descending_parser(G, T= None, firsts = None, follows = None):

    if T is None:

        if firsts is None:
            firsts = compute_firsts(G)

        if follows is None:
            follows = compute_follows(G, firsts)

        T = build_table_parser_ll1(G, firsts, follows)

    def parser(w):

        stack = [G.eof, G.start_non_terminal]
        cursor = 0
        output = []

        while True:

            top = stack.pop()
            c = w[cursor]

            if top.is_epsilon:
                pass

            elif top.is_terminal:

                if top != c:
                    print("Invalid input text")
                    return

                if top == G.eof:
                    break

                cursor += 1

            else:

                production = T[top, c][0]
                output.append(production)
                production = list(production.right)
                stack.extend(production[::-1])

        return output

    return parser


def non_recursive_descending_parser_fixed(G, M):
    parser = non_recursive_descending_parser(G, M)
    def update(tokens):
        return parser([t.reg_type for t in tokens])
    return update

def evaluate_left_parse(left_parse, tokens):

    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)

    return result


def evaluate(production, left_parse, tokens, inherited_value=None):

    _, right = production
    attributes = production.attributes

    synteticed = [None] * (len(right) + 1)
    inherited = [None] * (len(right) + 1)

    inherited[0] = inherited_value

    for i, symbol in enumerate(right, 1):

        # In case of Terminal syntetice their value writing the token lexeme
        if symbol.is_terminal:
            synteticed[i] = next(tokens).reg_exp

        # In case of NonTerminal get the inherited attribute and syntetice call recursively
        # in the next production
        else:
            next_production = next(left_parse)
            attr = attributes[i]
            if attr is not None:
                inherited[i] = attr(inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])

    # Return the results of the computed attributes
    attr = attributes[0]
    if attr is None:
        return None
    return attr(inherited, synteticed)
