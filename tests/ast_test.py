from core import SymbolNode, ClosureNode, Automaton, closure_automaton, \
    nfa_to_dfa

def test_ast():
    s = SymbolNode ("a")
    c = ClosureNode(s)
    aut = c.evaluate()
    aut = Automaton(2, 0, [1], [(0, 'a', [1])])
    dfa = nfa_to_dfa(closure_automaton(aut))

    assert dfa.recognize('')
    assert dfa.recognize('a')
    assert dfa.recognize('aa')
    assert dfa.recognize('aaa')
