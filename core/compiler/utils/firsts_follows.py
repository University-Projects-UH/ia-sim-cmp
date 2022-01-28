from ..grammar.grammar import *

def firsts(productions, terminals, non_terminals):

    res = {item: [] for item in non_terminals}
    marks = {item: False for item in non_terminals}
    for x in non_terminals:
        first_of_elem(x, productions, terminals, non_terminals, res, marks)
    return res
    
def first_of_elem(x, productions, terminals, non_terminals, res, marks):

    got_epsilon = False

    if isinstance(x, Epsilon):
        got_epsilon = True
        return [x], got_epsilon

    if isinstance(x, Terminal):
        return [x], got_epsilon
    
    if not marks[x]:
        marks[x] = True
        for p in productions:
            if p.left == x:
                y = p.right
                index = 0
                eps = True
                while eps and len(y) > index:
                    print("left: " + str(x) + " right: " + str(y[0]))
                    first_y, eps = first_of_elem(y[index], productions, terminals, non_terminals, res, marks)
                    if eps:
                        got_epsilon = True
                    for i in first_y:
                        if i not in res[x]:
                            res[x].append(i)
                    index += 1
        return res[x], got_epsilon
    else:
        for i in res[x]:
            if isinstance(i, Epsilon):
                return res[x], True
        return res[x], False

### Testing the algorithm to compute the firsts with the example of the conference

# e = Epsilon()

# t1 = Terminal("+")
# t2 = Terminal("*")
# t3 = Terminal("(")
# t4 = Terminal(")")
# t5 = Terminal("i")

# n0 = NonTerminal("S")
# n1 = NonTerminal("E")
# n2 = NonTerminal("T")
# n3 = NonTerminal("X")
# n4 = NonTerminal("Y")
# n5 = NonTerminal("F")

# p0 = Production(n0, [n1])
# p1 = Production(n1, [n2, n3])
# p2 = Production(n3, [t1, n2, n3])
# p3 = Production(n3, [e])
# p4 = Production(n2, [n5, n4])
# p5 = Production(n4, [t2, n5, n4])
# p6 = Production(n4, [e])
# p7 = Production(n5, [t3, n1, t4])
# p8 = Production(n5, [t5])

# productions = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
# terminals = [t1, t2, t3, t4, t5]
# non_terminals = [n0, n1, n2, n3, n4, n5]

# x = firsts(productions, terminals, non_terminals)

# print(x)