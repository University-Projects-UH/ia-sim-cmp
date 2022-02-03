from .automaton import Automaton

class DFA(Automaton):
    def __init__(self, states, start_state, finals_states, transitions):
        super().__init__(states, start_state, finals_states, transitions)

    def move_to(self, state, c):
        ends_array = self.get_ends_array_by_state_c(state, c)
        if(len(ends_array)):
            return ends_array[0]
        return None

    def recognize(self, pattern):
        state = self.start_state
        for c in pattern:
            state = self.move_to(state, c)
            if(state is None):
                return False
        return state in self.finals_states

