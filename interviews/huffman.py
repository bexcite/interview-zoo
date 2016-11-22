'''
Tutorial:
https://www.siggraph.org/education/materials/HyperGraph/video/mpeg/mpegfaq/huffman_tutorial.html
'''

import struct


class Node(object):

    def __init__(self, frequency, value=None, left=None, right=None):
        self.frequency = frequency
        self.value = value
        self.left = left
        self.right = right
        self.parent = None  # Set manually

    def is_leaf(self):
        return self.value is not None

    def children(self):
        children = []
        if self.left:
            children.append(self.left)
        if self.right:
            children.append(self.right)
        return children

    def __repr__(self):
        return '(%d, %s) -> %s' % (self.frequency, str(self.value),
                                   self.children())


def create_tree(items):
    if not items:
        return None

    processing = [Node(f, v) for f, v in items]
    while len(processing) > 1:
        processing = sorted(processing, key=lambda n: n.frequency)
        n1, n2 = processing[:2]
        processing = processing[2:]

        if n1.frequency < n2.frequency:
            parent = Node(n1.frequency + n2.frequency, left=n1, right=n2)
        else:
            parent = Node(n1.frequency + n2.frequency, left=n2, right=n1)

        # Set parents
        n1.parent = parent
        n2.parent = parent

        processing.append(parent)

    assert len(processing) == 1
    return processing[0]


def get_encodings(tree):
    encodings = {}

    def visit(node, prefix):
        if not node:
            return
        if node.is_leaf():
            encodings[node.value] = prefix
        visit(node.left, prefix + '0')
        visit(node.right, prefix + '1')

    visit(tree, '')

    return encodings


def compress(integers, encodings):
    return ''.join(encodings[i] for i in integers)


def pack_into_file(path, integers, items):
    encodings = get_encodings(create_tree(items))
    bits = compress(integers, encodings)
    chars = []
    for i in xrange(0, len(bits), 8):
        # FIXME(usmanm): Incomplete last byte needs to be properly written
        byte_str = bits[i:i + 8]
        byte = int(byte_str, 2)
        assert byte < 256
        chars.append(chr(byte))
    with open(path, 'w') as f:
        # Write # of unique chars
        s = struct.Struct('c')
        f.write(s.pack(chr(len(items))))
        # Write frequencies
        for item in items:
            s = struct.Struct('c c')
            f.write(s.pack(*map(lambda i: chr(i), item)))
        # Write comrpessed string
        f.write(''.join(chars))


def unpack_from_file(path):
    with open(path) as f:
        # Get number of unique chars
        s = struct.Struct('c')
        num_bytes = ord(s.unpack(f.read(s.size))[0])
        # Read frequencies
        items = []
        for _ in xrange(num_bytes):
            s = struct.Struct('c c')
            items.append(map(lambda c: ord(c), s.unpack(f.read(s.size))))
        chars = f.read()

    # Create tree
    encodings = get_encodings(create_tree(items))

    # Decode
    bits = ''.join(bin(ord(char))[2:] for char in chars)
    integers = []
    decodings = {v: k for k, v in encodings.iteritems()}
    code = ''
    for bit in bits:
        code += bit
        if code in decodings:
            integers.append(decodings[code])
            code = ''
    return integers


if __name__ == '__main__':
    items = [(5, 1), (7, 2), (10, 3), (15, 4), (20, 5), (45, 6)]
    pack_into_file('huff', [4, 1, 2, 6], items)
    unpack_from_file('huff')
