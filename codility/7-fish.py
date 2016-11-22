'''
You are given two non-empty zero-indexed arrays A and B consisting of N
integers. Arrays A and B represent N voracious fish in a river, ordered
downstream along the flow of the river. The fish are numbered from 0 to N - 1,
fish number P is represented by A[P] and B[P], and if P < Q then fish P is
initially upstream of fish Q. Initially, each fish has a unique position. Array
A contains the sizes of the fish. All its elements are > unique. Array B
contains the directions of the fish. It contains only 0s and/or 1s, where:

0 represents a fish flowing upstream
1 represents a fish flowing downstream
If two fish move in opposite directions and there are no other (living) fish
between them, they will eventually meet each other. Then only one fish can stay
alive - the larger fish eats the smaller one. More precisely, we say that two
fish P and Q meet each other when P < Q, B[P] = 1 and B[Q] = 0, and there are
no living fish between them. After they meet:

If A[P] > A[Q] then P eats Q, and P will still be flowing downstream,
If A[Q] > A[P] then Q eats P, and Q will still be flowing upstream.
We assume that all the fish are flowing at the same speed. That is, fish moving
in the same direction never meet. The goal is to calculate the number of fish
that will stay alive.

For example, consider arrays A and B such that:

A[0] = 4    B[0] = 0
A[1] = 3    B[1] = 1
A[2] = 2    B[2] = 0
A[3] = 1    B[3] = 0
A[4] = 5    B[4] = 0

Initially all the fish are alive and all except fish number 1 are moving
upstream. Fish > number 1 meets fish number 2 and eats it, then it meets fish
number 3 and eats it too. Finally, it meets fish number 4 and is eaten by it.
The remaining two fish, numbers 0 and 4, never meet and therefore stay alive.

Write a function:

class Solution { public int solution(int[] A, int[] B); }
that, given two non-empty zero-indexed arrays A and B consisting of N integers,
returns the number of fish that will stay alive.

For example, given the arrays shown above, the function should return 2, as
explained above.

Assume that:

N is an integer within the range [1..100,000], where each element of array A is
an integer within the range [0..1,000,000,000], where each element of array B
is an integer that can have one of the following values: 0, 1, where the
elements of A are all distinct.

Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not
counting the storage required for input arguments).
'''


def solution(A, B):
    survivors = []
    i = len(A) - 1
    while i >= 0:
        fish = (A[i], B[i])
        last = survivors[-1] if survivors else (0, 1)  # Downstream sentinel
        i -= 1
        # If fish ahead of us is going downstream, or we are going upstream
        # there is no conflict, since fish won't ever meet
        if last[1] or not fish[1]:
            survivors.append(fish)
            continue
        # Are we the smaller fish? Die x_x
        if last[0] > fish[0]:
            continue
        # Eat the last fish and retry us on the one before it
        survivors.pop()
        i += 1
    return len(survivors)


if __name__ == '__main__':
    assert solution([4, 3, 2, 1, 5], [0, 1, 0, 0, 0]) == 2
    assert solution([4, 3, 2, 1, 5], [0, 0, 0, 0, 1]) == 5
