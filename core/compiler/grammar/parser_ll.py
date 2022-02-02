
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

