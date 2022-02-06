from core import compute_firsts, compute_follows
from .parser_shift_reduce import ShiftReduceParser
from core import nfa_to_dfa, Automaton
from .Item import Item

def build_LR0_automaton(G):

    start_production = G.start_non_terminal.productions[0]
    start_item = Item(start_production, 0)

    aut_transitions = []
    states = 1

    stack = [start_item]
    visited = { start_item: 0 }

    while len(stack):
        current_item = stack.pop()
        if current_item.CanReduce:
            continue

        current_state = visited[current_item]

        next_item = current_item.NextItem()
        if next_item not in visited.keys():
            states += 1
            visited[next_item] = states
            stack.append(next_item)

        next_symbol = current_item.NextSymbol
        aut_transitions.append((current_state, next_symbol.name, [visited[next_item]]))

        for prod in G.productions:
            if next_symbol == prod.left:
                item = Item(prod, 0)
                if item not in visited.keys():
                    states += 1
                    visited[item] = states
                    stack.append(item)
                aut_transitions.append((current_state, '', visited[item]))

    aut = Automaton(states, 0, range(states), aut_transitions)
    for state, item in visited.items():
        aut.put_items(item, [state])

    return aut

class SLR1Parser(ShiftReduceParser):

    def build_parsing_table(self):
        G = self.grammar.AugmentedGrammar()
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        aut = nfa_to_dfa(build_LR0_automaton(G))

        for state in range(aut.states):
            for item in aut.items[state]:

                if item.CanReduce:
                    if item.production.left == G.start_non_terminal:
                        self._register(self.action_table, (state, G.eof), (SLR1Parser.OK, None))
                    else:
                        for symbol in follows[item.production.left]:
                            self._register(self.action_table, (state, symbol), (SLR1Parser.REDUCE, item.production))
                else:
                    next_symbol = item.NextSymbol
                    key = (state, next_symbol)
                    next_state = aut.move_from(state, next_symbol)
                    if next_symbol.is_terminal:
                        self._register(self.action_table, key, (SLR1Parser.SHIFT, next_state))
                    else:
                        self._register(self.goto_table, key, next_state)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
