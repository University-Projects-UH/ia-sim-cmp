from .dfa import DFA
from .automaton import Automaton

# set of states of the NFA to which there is a transition with the input
# character 'c' from some state of states_array.
def move(automaton, states_array, c):
    moves = set()
    for state in states_array:
        ends_array = automaton.get_ends_array_by_state_c(state, c)
        moves.update(ends_array)
    return moves

# set of reachable states from an states arrary only using epsilon transitions
def get_epsilon_closure(automaton, states):
    epsilon_closure = set(states)
    stack = list(states)
    while len(stack):
        state = stack.pop()
        epsilon_ends_array = automaton.get_epsilon_transitions(state)
        for state in epsilon_ends_array:
            if state not in epsilon_closure:
                stack.append(state)
                epsilon_closure.add(state)

    return epsilon_closure

class DFANode():
    def __init__(self, states):
        self.states = states

    def __eq__(self, other):
        return self.states == other.states

def nfa_to_dfa(automaton):
    new_transitions = []
    start_node = DFANode(list(get_epsilon_closure(automaton, [automaton.start_state])))
    start_node.id = 0
    node_array = [start_node]
    stack = [start_node]
    while len(stack):
        node = stack.pop()
        for c in automaton.universe:
            move_state_c = move(automaton, node.states, c)
            new_node = DFANode(list(get_epsilon_closure(automaton, move_state_c)))
            if len(new_node.states) == 0:
                continue

            founded = False
            for nodei in node_array:
                if(nodei == new_node):
                    new_node = nodei
                    founded = True
                    break
            if(founded is False):
                new_node.id = len(node_array)
                stack.append(new_node)
                node_array.append(new_node)

            new_transitions.append((node.id, c, [new_node.id]))

    finals_states = []
    for node in node_array:
        is_final = False
        for state in node.states:
            is_final = is_final or (state in automaton.finals_states)
        if(is_final):
            finals_states.append(node.id)

    dfa = DFA(len(node_array), 0, finals_states, new_transitions)
    return dfa

def union_automatas(aut_a, aut_b):
    aux = aut_a.states + 1
    new_final_state = aut_b.states + aux
    transitions = [(0, '', [1, aux])]
    states = new_final_state + 1

    a_transitions = aut_a.transitions
    for a_state in a_transitions:
        for c in a_transitions[a_state]:
            ends_array = [1 + end_state for end_state in a_transitions[a_state][c]]
            transitions.append((a_state + 1, c, ends_array))

    b_transitions = aut_b.transitions
    for b_state in b_transitions:
        for c in b_transitions[b_state]:
            ends_array = [aux + end_state for end_state in b_transitions[b_state][c]]
            transitions.append((a_state + aux, c, ends_array))

    for a_final_state in aut_a.finals_states:
        transitions.append((a_final_state + 1, '', [new_final_state]))

    for b_final_state in aut_b.finals_states:
        transitions.append((b_final_state + aux, '', [new_final_state]))

    return Automaton(states, 0, [new_final_state], transitions)

def concat_automatas(aut_a, aut_b):
    aux = aut_a.states
    new_final_state = aut_b.states + aux
    transitions = [(0, '', [1, aux])]
    states = new_final_state + 1

    a_transitions = aut_a.transitions
    for a_state in a_transitions:
        for c in a_transitions[a_state]:
            ends_array = [end_state for end_state in a_transitions[a_state][c]]
            transitions.append((a_state, c, ends_array))

    b_transitions = aut_b.transitions
    for b_state in b_transitions:
        for c in b_transitions[b_state]:
            ends_array = [aux + end_state for end_state in b_transitions[b_state][c]]
            transitions.append((a_state + aux, c, ends_array))

    for a_final_state in aut_a.finals_states:
        transitions.append((a_final_state, '', [aut_b.start + aux]))

    for b_final_state in aut_b.finals_states:
        transitions.append((b_final_state + aux, '', [new_final_state]))

    return Automaton(states, 0, [new_final_state], transitions)
