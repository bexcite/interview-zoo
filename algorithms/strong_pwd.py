'''
A password is considered strong if below conditions are all met:

It has at least 6 characters and at most 20 characters.
It must contain at least one lowercase letter, at least one uppercase letter,
and at least one digit.
It must NOT contain three repeating characters in a row ('...aaa...' is weak,
but '...aa...a...' is strong, assuming other conditions are met).
Write a function strongPasswordChecker(s), that takes a string s as input, and
return the MINIMUM change required to make s a strong password. If s is already
strong, return 0.

Insertion, deletion or replace of any one character are all considered as one
change.
'''
import string


class Solution(object):

    def strongPasswordChecker(self, s):
        '''
        :type s: str
        :rtype: int
        '''
        has_digit = False
        has_upper = False
        has_lower = False
        run_length = 0
        last = None
        runs = []
        for i, ch in enumerate(s):
            if ch == last:
                run_length += 1
            else:
                if run_length >= 3:
                    runs.append(run_length)
                run_length = 1
            has_digit = has_digit or ch in string.digits
            has_lower = has_lower or ch in string.ascii_lowercase
            has_upper = has_upper or ch in string.ascii_uppercase
            last = ch
        if run_length >= 3:
            runs.append(run_length)

        runs.sort()

        num_missing = 3 - (int(has_digit) + int(has_lower) + int(has_upper))
        num_to_add = max(0, 6 - len(s))
        num_to_remove = max(0, len(s) - 20)
        total = 0

        for i, run in enumerate(runs):
            if num_to_add:
                num_needed = run / 3
                num_used = min(num_to_add, num_needed)
                num_missing = max(num_missing - num_used, 0)
                num_to_add -= num_used
                run -= 3 * num_used
                total += num_used
            if num_missing:
                num_needed = run / 3
                num_used = min(num_missing, num_needed)
                num_missing -= num_used
                run -= 3 * num_used
                total += num_used
            if run >= 3:
                runs[i] = run
            else:
                runs[i] = 0

        while num_to_remove and sum(runs):
            runs = filter(None, runs)
            for i, run in enumerate(runs):
                if run / 3 > (run - 1) / 3:
                    runs[i] -= 1
                    num_to_remove -= 1
                    total += 1
                    if runs[i] < 3:
                        runs[i] = 0
                    break
            else:
                runs = sorted(runs, key=lambda r: r % 3)
                runs[0] -= 1
                if runs[0] < 3:
                    runs[0] = 0
                num_to_remove -= 1
                total += 1

        if num_missing:
            num_used = min(num_missing, num_to_add)
            num_missing -= num_used
            num_to_add -= num_used
            total += num_used

        total += num_missing + num_to_add + num_to_remove
        total += sum(run / 3 for run in runs)

        return total


if __name__ == '__main__':
    s = Solution()
    assert s.strongPasswordChecker('') == 6
    assert s.strongPasswordChecker('lollll1') == 1
    assert s.strongPasswordChecker('aaa111') == 2
    assert s.strongPasswordChecker('1111111111') == 3
    assert s.strongPasswordChecker('1234567890123456Baaaaa') == 3
    assert s.strongPasswordChecker('...') == 3
    assert s.strongPasswordChecker('aaaabbaaabbaaa123456A') == 3
    assert s.strongPasswordChecker('AAAAAABBBBBB123456789a') == 4
    assert s.strongPasswordChecker('aaaaaaaAAAAAA6666bbbbaaaaaaABBC') == 13
