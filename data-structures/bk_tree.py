def levenshtein_distance(src, target):
    if not min(len(src), len(target)):
        return max(len(src), len(target))

    dist = min(levenshtein_distance(src[1:], target) + 1,
               levenshtein_distance(src, target[1:]) + 1)

    if src[0] == target[0]:
        dist = min(dist, levenshtein_distance(src[1:], target[1:]))
    else:
        dist = min(dist, levenshtein_distance(src[1:], target[1:]) + 1)

    return dist


class Node(object):

    def __init__(self, value):
        self.value = value
        self.children = {}


class BKTree(object):

    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        node = self.root
        dist = levenshtein_distance(node.value, value)
        while dist in node.children:
            node = node.children[dist]
            dist = levenshtein_distance(node.value, value)
        if dist:
            node.children[dist] = Node(value)

    def _find(self, node, value, tolerance, result):
        dist = levenshtein_distance(node.value, value)
        if dist <= tolerance:
            result.append(node.value)
        for d, child in node.children.iteritems():
            if abs(d - dist) <= tolerance:
                self._find(child, value, tolerance, result)

    def find(self, value, tolerance=0):
        if self.root is None:
            return []
        node = self.root
        result = []
        self._find(node, value, tolerance, result)
        return result


if __name__ == '__main__':
    b = BKTree()

    b.insert('book')
    b.insert('books')
    b.insert('cake')
    b.insert('boo')
    b.insert('cape')
    b.insert('boon')
    b.insert('cook')
    b.insert('cart')

    assert b.find('caqe', tolerance=1) == ['cake', 'cape']
