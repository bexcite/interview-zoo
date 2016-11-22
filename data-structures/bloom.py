import array
import md5
import struct


def _hash(item):
    item = str(item)  # Use serialized value for item
    h0 = int(md5.md5(item).hexdigest(), 16)
    h1 = int(md5.md5(item + 'salt').hexdigest(), 16)
    return (h0, h1)


class BloomFilter(object):

    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.array = array.array('l', (0 for _ in xrange((self.m / 64) + 1)))

    def _bit_mask(self, i):
        return 1 << (i % 64)

    def _bit_idx(self, i):
        return (i % self.m) / 64

    def add(self, item):
        h0, h1 = _hash(item)
        for i in xrange(self.k):
            h = h0 + i * h1
            self.array[self._bit_idx(h)] |= self._bit_mask(h)

    def contains(self, item):
        h0, h1 = _hash(item)
        for i in xrange(self.k):
            h = h0 + i * h1
            if not self.array[self._bit_idx(h)] & self._bit_mask(h):
                return False
        return True

    def union(self, other):
        for i in other.array:
            self.array |= i

    def intersection(self, other):
        for i in other.array:
            self.array &= i

    def equals(self, other):
        return (self.m == other.m and
                self.k == other.k and
                self.array == other.array)

    def to_file(self, path):
        with open(path, 'w') as f:
            s = struct.Struct('I I')
            f.write(s.pack(self.m, self.k))
            self.array.tofile(f)

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            s = struct.Struct('I I')
            m, k = s.unpack(f.read(s.size))
            b = BloomFilter(m, k)
            b.array = array.array('l', [])
            b.array.fromfile(f, m / 64 + 1)
            return b
