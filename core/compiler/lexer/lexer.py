from .token import Token
from .regex import Regex
from .automaton.utils import nfa_to_dfa, union_automatas

class Lexer:
    # regex array contains tuples (type, regex)
    def __init__(self, regex_array, eof):
        self.eof = eof
        self.regexs_aut = self._build_regexs(regex_array)
        self.automaton = self._build_automaton()

    def _build_regexs(self, regex_array):
        regexs_aut = []
        for i in range(len(regex_array)):
            token_type, regex = regex_array[i]
            # this is an dfa
            regex_aut = Regex(regex).automaton
            for final_state in regex_aut.finals_states:
                regex_aut.put_tag(final_state, (i, token_type))
            regexs_aut.append(regex_aut)
        return regexs_aut

    def _build_automaton(self):
        aut_result = self.regexs_aut[0]
        aut_count = len(self.regexs_aut)
        for i in range(1, aut_count):
            aut = self.regexs_aut[i]
            aut_result = union_automatas(aut_result, aut)
        return nfa_to_dfa(aut_result)

    def _walk(self, string):
        aut = self.automaton
        state = aut.start_state
        final = state if aut.is_final(state) else None
        final_lex = lex = ''
        for symbol in string:
            lex += symbol
            state = aut.move_from(state, symbol)
            if(state is None):
                break
            if aut.is_final(state):
                final = state
                final_lex = lex

        return final, final_lex

    def _tokenize(self, text):
        aut = self.automaton
        while text:
            final_state, lex = self._walk(text)
            if(final_state == None):
                break
            assert final_state != None, "The text does not match with the defined gramatic"

            assert len(lex) != 0, 'Error'

            text = text[len(lex):]
            yield lex, aut.get_tag(final_state)[1]

        yield '$', self.eof

    def __call__(self, text):
        return [Token(lex, ttype) for lex, ttype in self._tokenize(text) ]
