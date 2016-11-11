'''
Given a string, sort it in decreasing order based on the frequency of
characters.
'''


def sort_chars(string):
    # Only need to store at most log(len(string)) bits per character since
    # that's enough to represent the max number of times a character can appear
    occurrences = [0] * 255
    for ch in string:
        occurrences[ord(ch)] += 1

    # Only need to store a bit string of max length 255 to represent which
    # characters appeared a certain number of times
    runs = [[] for _ in xrange(len(string) + 1)]
    for byte, occurrence in enumerate(occurrences):
        if not occurrence:
            continue
        runs[occurrence].append(chr(byte))

    # Here, we basically have to print characters for all the set positions for
    # each bit string. Iterate backwards to print most repeating characters
    # first
    out = ''
    for i in range(len(runs) - 1, -1, -1):
        for ch in runs[i]:
            out = '%s%s' % (out, ch * i)

    return out


if __name__ == '__main__':
    assert sort_chars('tree') in ['eetr', 'eert']
    assert sort_chars('cccaaa') in ['cccaaa', 'aaaccc']
    assert sort_chars('Aabb') in ['bbAa', 'bbaA']
