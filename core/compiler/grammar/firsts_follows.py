
from utils import ContainerSet

##################################################################

# Rules:

# 1- If X -> W1 | W2 | ... | Wn      =>      First(X) = Union(First(Wi))
# 2- If X -> epsilon       =>      epsilon in First(X)
# 3- If W = xZ where x is Terminal     =>      First(W) = {x}
# 4- If W = YZ where Y is NonTerminal y Z is an orational form     =>      First(Y) in First(W)
# 5- If W = YZ and epsilon in First(Y)     =>      First(Z) in First(W)

##################################################################

def compute_local_first(firsts, alpha):

    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.is_epsilon
    except:
        alpha_is_epsilon = False

    # Rule 2
    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    # Rules 1, 3, 4, 5
    else:
        for symbol in alpha:
            first_alpha.update(firsts[symbol])
            if not firsts[symbol].contains_epsilon:
                break
            else:
                first_alpha.set_epsilon()

    return first_alpha

def compute_firsts(G):

    firsts = {}
    change = True

    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for non_terminal in G.non_terminals:
        firsts[non_terminal] = ContainerSet()

    while change:

        change = False

        for production in G.productions:

            X = production.left
            alpha = production.right

            first_X = firsts[X]

            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)

            change = first_alpha.hard_update(local_first) or change
            change = first_X.hard_update(local_first) or change
    
    return firsts
