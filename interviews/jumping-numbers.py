'''
Print all Jumping Numbers smaller than or equal to a given value

A number is called as a Jumping Number if all adjacent digits in it differ by 1
The difference between '9' and '0' is not considered as 1.
'''


def solution(n):
    q = range(10)
    jumping = []
    while q:
        i = q.pop(0)
        lsd = i % 10
        prev, next_ = (lsd - 1) % 10, (lsd + 1) % 10

        jumping.append(i)

        # 0 has no adjacent numbers
        if i == 0:
            continue

        # 9 is not adjacent to 0
        if prev != 9:
            prev_number = (10 * i) + prev
            if prev_number <= n:
                q.append(prev_number)
        # 0 is not adjacent to 9
        if next_:
            next_number = (10 * i) + next_
            if next_number <= n:
                q.append(next_number)

    return jumping

if __name__ == '__main__':
    assert solution(33) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 21, 23, 32]
