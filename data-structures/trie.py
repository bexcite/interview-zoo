class Node(object):

    def __init__(self, value=None):
        self.value = None
        self.children = {}


class Trie(object):

    def __init__(self, delimiter='$'):
        self.root = Node(None)
        self.delimiter = delimiter

    def insert(self, key, value=None):
        node = self.root
        for ch in key + self.delimiter:
            if ch not in node.children:
                node.children[ch] = Node()
            node = node.children[ch]
        node.value = value

    def find(self, key):
        node = self.root
        for ch in key + self.delimiter:
            if ch not in node.children:
                raise KeyError
            node = node.children[ch]
        return node.value


if __name__ == '__main__':
    t = Trie()
    t.insert('apple', 0)
    t.insert('apricot', 1)
    t.insert('bottle', 2)

    assert t.find('apple') == 0
    assert t.find('apricot') == 1
    assert t.find('bottle') == 2

    try:
        t.find('error')
        assert False
    except KeyError:
        pass
