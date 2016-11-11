'''
Design and implement a data structure for Least Recently Used (LRU) cache. It
should support the following operations: get and set.

get(key) - Get the value (will always be positive) of the key if the key exists
in the cache, otherwise return -1.

set(key, value) - Set or insert the value if the key is not already present.
When the cache reached its capacity, it should invalidate the least recently
used item before inserting a new item.
'''


class Node(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        return '(%s, %d)' % (self.key, self.value)


class LRUCache(object):

    def __init__(self, capacity):
        '''
        :type capacity: int
        '''
        self.capacity = capacity
        self.items = {}
        self.head = None
        self.tail = None

    def check(self):
        if not len(self.items):
            return

        assert self.head
        assert self.head.prev == self.tail
        assert self.tail
        assert self.tail.next == self.head

        node = self.head
        num_nodes = 1
        while node != self.tail:
            next_node = node.next
            assert next_node.prev == node
            node = next_node
            num_nodes += 1
        assert num_nodes == len(self.items)

    def get(self, key):
        '''
        :rtype: int
        '''
        node = self.items.get(key)
        if node is None:
            return -1

        # If we're already the head, bail
        if self.head == node:
            return node.value

        # Plop node
        node.prev.next = node.next
        node.next.prev = node.prev

        # If removing tail, set new tail
        if self.tail == node:
            self.tail = node.prev

        # Set new head
        node.next = self.head
        self.head.prev = node
        node.prev = self.tail
        self.tail.next = node
        self.head = node

        return node.value

    def set(self, key, value):
        '''
        :type key: int
        :type value: int
        :rtype: nothing
        '''
        # 0 capacity? Noop.
        if not self.capacity:
            return

        # If we already have the key, update it's value and mark as lru
        if key in self.items:
            self.items[key].value = value
            self.get(key)
            return

        # Are we full? Kick out tail element
        if len(self.items) == self.capacity:
            old_tail = self.tail
            old_tail.prev.next = old_tail.next
            old_tail.next.prev = old_tail.prev
            self.tail = old_tail.prev
            del self.items[old_tail.key]

        assert len(self.items) < self.capacity

        node = Node(key, value)
        self.items[key] = node

        if len(self.items) == 1:
            node.next = node.prev = node
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            node.prev = self.tail
            self.tail.next = node
            self.head = node

if __name__ == '__main__':
    lru = LRUCache(2)
    lru.set('a', 1)
    lru.set('b', 2)
    assert lru.get('a') == 1
    assert lru.get('b') == 2
    assert lru.get('c') == -1
    lru.set('c', 3)
    assert lru.get('a') == -1
    assert lru.get('b') == 2
    assert lru.get('c') == 3

    lru = LRUCache(1)
    lru.set('a', 1)
    lru.set('b', 2)
    assert lru.get('a') == -1
    assert lru.get('b') == 2
    assert lru.get('c') == -1
    lru.set('c', 3)
    assert lru.get('a') == -1
    assert lru.get('b') == -1
    assert lru.get('c') == 3

    lru = LRUCache(10)

    def set(key, value):
        lru.set(key, value)
        lru.check()

    def get(key):
        value = lru.get(key)
        lru.check()
        return value

    [set(10, 13), set(3, 17), set(6, 11), set(10, 5), set(9, 10), get(13),
     set(2, 19), get(2), get(3), set(5, 25), get(8), set(9, 22), set(5, 5),
     set(1, 30), get(11), set(9, 12), get(7), get(5), get(8), get(9),
     set(4, 30), set(9, 3), get(9), get(10), get(10), set(6, 14), set(3, 1),
     get(3), set(10, 11), get(8), set(2, 14), get(1), get(5), get(4),
     set(11, 4), set(12, 24), set(5, 18), get(13), set(7, 23), get(8), get(12),
     set(3, 27), set(2, 12), get(5), set(2, 9), set(13, 4), set(8, 18),
     set(1, 7), get(6), set(9, 29), set(8, 21), get(5), set(6, 30), set(1, 12),
     get(10), set(4, 15), set(7, 22), set(11, 26), set(8, 17), set(9, 29),
     get(5), set(3, 4), set(11, 30), get(12), set(4, 29), get(3), get(9),
     get(6), set(3, 4), get(1), get(10), set(3, 29), set(10, 28), set(1, 20),
     set(11, 13), get(3), set(3, 12), set(3, 8), set(10, 9), set(3, 26),
     get(8), get(7), get(5), set(13, 17), set(2, 27), set(11, 15), get(12),
     set(9, 19), set(2, 15), set(3, 16), get(1), set(12, 17), set(9, 1),
     set(6, 19), get(4), get(5), get(5), set(8, 1), set(11, 7), set(5, 2),
     set(9, 28), get(1), set(2, 2), set(7, 4), set(4, 22), set(7, 24),
     set(9, 26), set(13, 28), set(11, 26)]
