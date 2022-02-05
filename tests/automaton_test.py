from core import Automaton, nfa_to_dfa, DFA, union_automatas, concat_automatas, \
    closure_automaton

def test_transform_nfa_to_dfa():
    automaton = Automaton(3, 0, [2], transitions=[
        (0, 'a', [0]),
        (0, 'b', [1]),
        (1, 'a', [2]),
        (1, 'b', [1]),
        (2, 'a', [0]),
        (2, 'b', [1]),
    ])

    automaton = nfa_to_dfa(automaton)
    assert automaton.recognize('ba')
    assert automaton.recognize('aababbaba')

    assert not automaton.recognize('')
    assert not automaton.recognize('aabaa')
    assert not automaton.recognize('aababb')

    dfa = nfa_to_dfa(Automaton(6, 0, [3, 5], transitions=[
        (0, '', [1, 2]),
        (1, '', [3]),
        (1, 'b', [4]),
        (2, 'a', [4]),
        (3, 'c', [3]),
        (4, '', [5]),
        (5, 'd', [5]),
    ]))
    assert dfa.states == 4
    assert len(dfa.finals_states) == 4

    assert not dfa.recognize('dddddd')
    assert not dfa.recognize('cdddd')
    assert not dfa.recognize('aa')
    assert not dfa.recognize('ab')
    assert not dfa.recognize('ddddc')

    assert dfa.recognize('')
    assert dfa.recognize('a')
    assert dfa.recognize('b')
    assert dfa.recognize('cccccc')
    assert dfa.recognize('adddd')
    assert dfa.recognize('bdddd')

def test_automatas_union():

    aut1 = Automaton(2, 0, [1], [(0, '1', [1])])
    aut2 = Automaton(2, 0, [1], [(0, '2', [1])])
    aut3 = Automaton(2, 0, [1], [(0, '3', [1])])

    un = union_automatas(aut1, aut2)
    un = union_automatas(un, aut3)
    dfa = nfa_to_dfa(un)
    assert dfa.recognize("1")
    assert dfa.recognize("2")
    assert dfa.recognize("3")

    automaton = DFA(2, 0, [1], transitions=[
        (0, 'a', [0]),
        (0, 'b', [1]),
        (1, 'a', [0]),
        (1, 'b', [1]),
    ])
    union = union_automatas(automaton, automaton)
    recognize = nfa_to_dfa(union).recognize

    assert union.states == 2 * automaton.states + 2

    assert recognize('b')
    assert recognize('abbb')
    assert recognize('abaaababab')

    assert not recognize('')
    assert not recognize('a')
    assert not recognize('abbbbaa')

def test_automatas_concat():
    automaton = DFA(2, 0, [1], transitions=[
        (0, 'a', [0]),
        (0, 'b', [1]),
        (1, 'a', [0]),
        (1, 'b', [1]),
    ])
    concat = concat_automatas(automaton, automaton)
    recognize = nfa_to_dfa(concat).recognize
    assert concat.states == 2 * automaton.states + 1

    assert recognize('bb')
    assert recognize('abbb')
    assert recognize('abaaababab')

    assert not recognize('')
    assert not recognize('a')
    assert not recognize('b')
    assert not recognize('ab')
    assert not recognize('aaaab')
    assert not recognize('abbbbaa')

def test_automaton_closure():
    automaton = DFA(2, 0, [1], transitions=[
        (0, 'a', [0]),
        (0, 'b', [1]),
        (1, 'a', [0]),
        (1, 'b', [1]),
    ])
    closure = closure_automaton(automaton)
    recognize = nfa_to_dfa(closure).recognize
    assert closure.states == automaton.states + 2

    assert recognize('')
    assert recognize('b')
    assert recognize('ab')
    assert recognize('bb')
    assert recognize('abbb')
    assert recognize('abaaababab')

    assert not recognize('a')
    assert not recognize('abbbbaa')
