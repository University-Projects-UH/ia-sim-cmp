from core import compute_firsts, compute_follows, ContainerSet, \
    compute_firsts, compute_local_first, DFA
from .Item import Item
from .parser_shift_reduce import ShiftReduceParser

def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.is_nonTerminal:
        return []

    lookaheads = ContainerSet()
    for preview in item.Preview():
        lookaheads.hard_update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    child_items = []
    for prod in next_symbol.productions:
        child_items.append(Item(prod, 0, lookaheads))
    return child_items

def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return { Item(x.production, x.position, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)

    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G):

    firsts = compute_firsts(G)
    firsts[G.eof] = ContainerSet(G.eof)

    start_production = G.start_non_terminal.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.eof,))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    items_arr = [frozenset(closure)]
    transitions = []
    states = 1

    stack = [start]
    visited = { start: 0 }

    while len(stack):
        current = stack.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.non_terminals:
            next_items = goto_lr1(items_arr[current_state], symbol, just_kernel=True)
            if not next_items:
                continue
            if(visited.__contains__(next_items)):
                next_state = visited[next_items]
            else:
                stack.append(next_items)
                closure = closure_lr1(next_items, firsts)
                items_arr.append(frozenset(closure))
                visited[next_items] = states
                next_state = states
                states += 1

            transitions.append((current_state, symbol.name, [next_state]))

    aut = DFA(states, 0, range(states), transitions)
    for state in range(states):
        aut.put_items(state, items_arr[state])

    return aut

class LR1Parser(ShiftReduceParser):
    def build_parsing_table(self):
        G = self.grammar.AugmentedGrammar(True)

        aut = build_LR1_automaton(G)

        for state in range(aut.states):
            for item in aut.items[state]:
                if item.CanReduce:
                    if item.production.left == G.start_non_terminal:
                        self._register(self.action_table, (state, G.eof), (LR1Parser.OK, None))
                    else:
                        for s in item.lookaheads:
                            self._register(self.action_table, (state, s), (LR1Parser.REDUCE, item.production))
                else:
                    next_symbol = item.NextSymbol
                    key = (state, next_symbol)
                    next_state = aut.move_from(state, next_symbol.name)
                    if next_symbol.is_terminal:
                        self._register(self.action_table, key, (LR1Parser.SHIFT, next_state))
                    else:
                        self._register(self.goto_table, key, next_state)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
