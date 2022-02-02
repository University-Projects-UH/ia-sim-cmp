
##################################################################

# Rules:

# 1- If X -> W, t in Terminals and t in First(W)    =>    T[X, t] = X -> W
# 2- If X -> W, t in terminals, epsilon in First(W) and t in Follow(X)   =>    T[X, t] = X -> W  

##################################################################

from firsts_follows import compute_firsts, compute_follows

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

def descending_not_recursive_parser(G, T= None, firsts = None, follows = None):

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
