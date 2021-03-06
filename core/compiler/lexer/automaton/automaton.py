class Automaton:
    # finals_states: finals states array
    # transitions: tuples array (first, c, ends_array) first -> c -> endi,
    # c is the transition character and endi belongs to ends array
    def __init__(self, states, start_state, finals_states, transitions):
        self.states = states
        self.tags = [None] * states
        self.items = [[] for _ in range(states)]
        self.start_state = start_state
        self.finals_states = finals_states
        self.transitions = {}
        self.universe = set()
        for state, c, ends_array in transitions:
            if(c != ''):
                self.universe.add(c)
            if(self.transitions.__contains__(state) == False):
                self.transitions[state] = {}
            if(self.transitions[state].__contains__(c) == False):
                self.transitions[state][c] = []
            self.transitions[state][c] += ends_array

    def get_ends_array_by_state_c(self, state, c):
        if(state >= self.states):
            raise Exception("The state does not exist on the automaton")
        if(self.transitions.__contains__(state) == False):
            return []
        if(self.transitions[state].__contains__(c)):
            return self.transitions[state][c]
        return []

    def get_epsilon_transitions(self, state):
        return self.get_ends_array_by_state_c(state, "")

    def get_items(self, state):
        return self.items[state]

    def put_items(self, state, items):
        if(items is None):
            return
        self.items[state] += items

    def put_tag(self, state, tag):
        if(self.tags[state] is None):
            self.tags[state] = tag
        elif(self.tags[state][0] > tag[0]):
            self.tags[state] = tag

    def get_tag(self, state):
        return self.tags[state]

    def is_final(self, state):
        return state in self.finals_states
