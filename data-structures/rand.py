'''
Design a data structure that supports all following operations in average O(1)
time.

Note: Duplicate elements are allowed.
insert(val): Inserts an item val to the collection.
remove(val): Removes an item val from the collection if present.
getRandom: Returns a random element from current collection of elements. The
probability of each element being returned is linearly related to the number of
same value the collection contains.
'''
from collections import defaultdict
import random

sentinel = object()


class RandomizedCollection(object):

    def __init__(self):
        '''
        Initialize your data structure here.
        '''
        self.array = []
        self.items = {}

    def check(self):
        assert len(self.items) <= len(self.array)
        for s in self.items.itervalues():
            for idx in s:
                assert idx < len(self.array)

    def insert(self, val):
        '''
        Inserts a value to the collection. Returns true if the collection did
        not already contain the specified element.
        :type val: int
        :rtype: bool
        '''
        exists = val in self.items
        if not exists:
            self.items[val] = set()

        # Both the following functions are amortized O(1) cost
        self.items[val].add(len(self.array))
        self.array.append(val)
        return not exists

    def remove(self, val):
        '''
        Removes a value from the collection. Returns true if the collection
        contained the specified element.
        :type val: int
        :rtype: bool
        '''
        if val not in self.items:
            return False

        # All these operations are O(1) amortized cost
        idx = self.items[val].pop()
        # Replace the value in array with last value in array
        last_val = self.array.pop()
        # Use discard here since val and last_val could be equal
        self.items[last_val].discard(len(self.array))
        if idx < len(self.array):
            self.array[idx] = last_val
            self.items[last_val].add(idx)
        # If this was the last occurrence of val, remove it from dict
        if not self.items[val]:
            del self.items[val]
        return True

    def getRandom(self):
        '''
        Get a random element from the collection.
        :rtype: int
        '''
        return random.choice(self.array)


if __name__ == '__main__':
    s = RandomizedCollection()
    for i in range(20):
        assert s.insert(i)
    for i in range(20):
        assert not s.insert(i)
    for i in range(0, 20, 2):
        assert s.remove(i)
    for i in range(0, 20, 2):
        assert not s.insert(i)
    for i in range(0, 20, 2):
        assert s.remove(i)
    for i in range(20):
        assert s.remove(i)
    for i in range(0, 20, 2):
        assert not s.remove(i)

    items = []
    for i in range(1000):
        items.append(s.getRandom())
    keys = defaultdict(int)
    for item in items:
        keys[item] += 1
    assert len(keys) == 10
    for v in keys.values():
        assert v >= 50
        assert v <= 150
