'''
Given two words (beginWord and endWord), and a dictionary's word list, find all
shortest transformation sequence(s) from beginWord to endWord, such that:

Only one letter can be changed at a time
Each intermediate word must exist in the word list
For example,

Given:
- beginWord = "hit"
- endWord = "cog"
- wordList = ["hot","dot","dog","lot","log"]

Return:
  [
    ["hit","hot","dot","dog","cog"],
    ["hit","hot","lot","log","cog"]
  ]

Note:
- All words have the same length.
- All words contain only lowercase alphabetic characters.
'''
from collections import defaultdict


class BinHeap(object):

    def __init__(self):
        self.items = [None]

    @property
    def num_items(self):
        return len(self.items) - 1

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

    def del_min(self):
        if not self.num_items:
            raise KeyError
        if self.num_items == 1:
            return self.items.pop(1)
        root = self.items[1]
        self.items[1] = self.items.pop(-1)
        self.perc_down(1)
        return root


def diff(src, target):
    d = 0
    for ch1, ch2 in zip(src, target):
        if ch1 != ch2:
            d += 1
    return d


def make_graph(beginWord, endWord, wordlist):
    graph = defaultdict(set)
    for i in range(len(wordlist)):
        a = wordlist[i]
        for j in range(i, len(wordlist)):
            b = wordlist[j]
            if diff(a, b) != 1:
                continue
            graph[a].add(b)
            graph[b].add(a)
        if diff(beginWord, a) == 1:
            graph[beginWord].add(a)
        if diff(endWord, a) == 1:
            graph[a].add(endWord)
    return graph


def dijkstra(start, end, graph):
    distances = {}
    predecessors = {}
    queue = BinHeap()

    # Start from begin
    queue.insert((0, start))
    distances[start] = 0
    predecessors[start] = None

    while queue.num_items:
        d, node = queue.del_min()

        if node == end:
            break

        for child in graph[node]:
            if child not in distances or distances[child] > d + 1:
                queue.insert((d + 1, child))
                distances[child] = d + 1
                predecessors[child] = [node]
            elif distances[child] == d + 1:
                predecessors[child].append(node)

    return predecessors


class Solution(object):

    def findLadders(self, beginWord, endWord, wordlist):
        '''
        :type beginWord: str
        :type endWord: str
        :type wordlist: Set[str]
        :rtype: List[List[int]]
        '''
        graph = make_graph(beginWord, endWord, list(wordlist))
        predecessors = dijkstra(beginWord, endWord, graph)

        incomplete = [[endWord]]
        paths = []
        while incomplete:
            path = incomplete.pop()
            first = path[0]
            if first == beginWord:
                paths.append(path)
                continue
            for p in predecessors.get(first, []):
                new_path = [p]
                new_path.extend(path)
                incomplete.append(new_path)
        return paths


if __name__ == '__main__':
    s = Solution()
    assert (s.findLadders('hit', 'cog',
                          set(['hot', 'dot', 'dog', 'lot', 'log'])) ==
            [['hit', 'hot', 'lot', 'log', 'cog'],
             ['hit', 'hot', 'dot', 'dog', 'cog']])
    assert s.findLadders('hot', 'dog', []) == []
