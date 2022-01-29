from grammar import *

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
                    #print("left: " + str(x) + " right: " + str(y[0]))
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

def follows(productions, terminals, non_terminals, end):

    res = {}
    for nt in non_terminals:
        res[nt] = []
        if isinstance(nt, InitialNonTerminal):
            res[nt].append(end)

    first_set = firsts(productions, terminals, non_terminals)

    for p in productions:
        r = p.right
        for i in range(len(r) - 1):
            if isinstance(r[i], NonTerminal):
                current = r[i]
                j = i + 1
                got_epsilon = True
                while j < len(r) and got_epsilon:
                    got_epsilon = False
                    next = r[j]
                    if isinstance(next, NonTerminal):
                        for k in first_set[next]:
                            if not isinstance(k, Epsilon) and k not in res[current]:
                                res[current].append(k)
                            elif isinstance(k, Epsilon):
                                got_epsilon = True
                        j += 1
                    elif next not in res[current]:
                        res[current].append(next)
    
    change = True

    while change:
        change = False
        for p in productions:
            l = p.left
            r = p.right
            for i in range(len(r) - 1, -1, -1):
                got_epsilon = False
                current = r[i]
                if isinstance(current, NonTerminal):
                    for j in res[l]:
                        if j not in res[current]:
                            res[current].append(j)
                            change = True
                        for f in first_set[current]:
                            if isinstance(f, Epsilon):
                                got_epsilon = True
                if not got_epsilon:
                    break

    return res

### Testing the algorithm to compute the firsts with the example of the conference

# e = Epsilon()
# end = End()

# t1 = Terminal("+")
# t2 = Terminal("*")
# t3 = Terminal("(")
# t4 = Terminal(")")
# t5 = Terminal("i")

# n0 = InitialNonTerminal("S")
# n1 = NonTerminal("E")
# n2 = NonTerminal("T")
# n3 = NonTerminal("X")
# n4 = NonTerminal("Y")
# n5 = NonTerminal("F")

# p0 = Production(n0, [n1, end])
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

# first = firsts(productions, terminals, non_terminals)
# follow = follows(productions, terminals, non_terminals, end)

# print(first)
# print(follow)

# end = End()

# t1 = Terminal("+")
# t2 = Terminal("*")
# t3 = Terminal("(")
# t4 = Terminal(")")
# t5 = Terminal("i")

# n0 = InitialNonTerminal("S")
# n1 = NonTerminal("E")
# n2 = NonTerminal("T")
# n3 = NonTerminal("F")

# p0 = Production(n0, [n1, end])
# p1 = Production(n1, [n1, t1, n2])
# p2 = Production(n1, [n2])
# p3 = Production(n2, [n2, t2, n3])
# p4 = Production(n2, [n3])
# p5 = Production(n3, [t3, n1, t4])
# p6 = Production(n3, [t5])

# productions = [p0, p1, p2, p3, p4, p5, p6]
# terminals = [t1, t2, t3, t4, t5]
# non_terminals = [n0, n1, n2, n3]

# first = firsts(productions, terminals, non_terminals)
# follow = follows(productions, terminals, non_terminals, end)

# print(first)
# print(follow)