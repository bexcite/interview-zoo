class BinHeap(object):

    def __init__(self):
        self.items = [None]

    @property
    def num_items(self):
        return len(self.items) - 1

    def check(self):
        for i in xrange(1, self.num_items / 2):
            item = self.items[i]
            ch1 = self.items[i * 2]
            if i * 2 < self.num_items:
                ch2 = self.items[i * 2 + 1]
            else:
                ch2 = ch1
            assert ch1 > item
            assert ch2 > item

    def perc_up(self, i):
        while i / 2:
            item = self.items[i]
            parent = self.items[i / 2]
            if parent < item:
                break
            self.items[i] = parent
            self.items[i / 2] = item
            i /= 2

    def min_child(self, i):
        if i * 2 == self.num_items:
            return i * 2
        elif self.items[i * 2] < self.items[i * 2 + 1]:
            return i * 2
        else:
            return i * 2 + 1

    def perc_down(self, i):
        while i <= self.num_items / 2:
            mc = self.min_child(i)
            child = self.items[mc]
            item = self.items[i]
            if item < child:
                break
            self.items[i] = child
            self.items[mc] = item
            i = mc

    def insert(self, item):
        self.items.append(item)
        self.perc_up(self.num_items)
        self.check()

    def del_min(self):
        if not self.num_items:
            raise KeyError
        if self.num_items == 1:
            return self.items.pop(1)
        root = self.items[1]
        self.items[1] = self.items.pop(-1)
        self.perc_down(1)
        self.check()
        return root

    def extend(self, items):
        self.items.extend(items)
        i = self.num_items / 2
        while i:
            self.perc_down(i)
            i -= 1
        self.check()


if __name__ == '__main__':
    h1 = BinHeap()
    items = [0, 9, 5, 6, 2, 3]
    for item in items:
        h1.insert(item)
    sorted_items = []
    for item in items:
        sorted_items.append(h1.del_min())
    assert sorted_items == sorted(sorted_items)

    h2 = BinHeap()
    h2.extend(items)
