from core import Regex

def test_regex():

    dfa = Regex('[1|2|5]').automaton
    assert dfa.recognize("1")
    assert dfa.recognize("2")
    assert dfa.recognize("5")

    dfa = Regex('a^[a|b]^cd| ε ', True).automaton

    assert dfa.recognize('')
    assert dfa.recognize('aaacd')
    assert dfa.recognize('cd')
    assert dfa.recognize('aaaaacd')
    assert dfa.recognize('bbbbbcd')
    assert dfa.recognize('bbabababcd')
    assert dfa.recognize('aaabbabababcd')

    assert not dfa.recognize('cda')
    assert not dfa.recognize('aaaaa')
    assert not dfa.recognize('bbbbb')
    assert not dfa.recognize('ababba')
    assert not dfa.recognize('cdbaba')
    assert not dfa.recognize('cababad')
    assert not dfa.recognize('bababacc')
