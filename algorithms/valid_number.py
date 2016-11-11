'''
Validate if a given string is numeric.

Some examples:
"0" => true
" 0.1 " => true
"abc" => false
"1 a" => false
"2e10" => true
'''
import string

allowed = set(string.digits) | set('+-e. ')


class State(object):
    INIT = set('e!')
    MINUS = set('&')
    FDIGIT = set('+-@')
    SDIGIT = set('+-e.#')
    SAFE_DOT = set('+-.$')
    DOT = set('+-. %')
    EXP = set('+-e. ^')
    ENDED = set(string.digits) | set('+-e.^')


class Solution(object):

    def isNumber(self, s):
        '''
        :type s: str
        :rtype: bool
        '''
        state = State.INIT
        for ch in s:
            # Is this character valid?
            if ch not in allowed:
                return False
            # Is this character disallowed in this state?
            if ch in state:
                return False
            if ch in string.digits:
                if (state is State.INIT or
                    state is State.FDIGIT or
                        state is State.MINUS):
                    state = State.FDIGIT
                else:
                    state = State.SDIGIT
            elif ch == '-' or ch == '+':
                state = State.MINUS
            elif ch == '.':
                if state is State.FDIGIT:
                    state = State.SAFE_DOT
                else:
                    state = State.DOT
            elif ch == 'e':
                state = State.EXP
            elif ch == ' ':
                if state is not State.INIT:
                    state = State.ENDED
        return (state is not State.INIT and
                state is not State.EXP and
                state is not State.DOT and
                state is not State.MINUS)


if __name__ == '__main__':
    s = Solution()
    for test in ['0', ' 0.1 ', '2e10', '1 ', '3.', '-1.', '46.e3']:
        assert s.isNumber(test)
    for test in ['.', 'e', '1 a', '0 .1', '. ', '+ 1', '+++']:
        assert not s.isNumber(test)
