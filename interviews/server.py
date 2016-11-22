from collections import defaultdict
import re

'''
You're running a pool of servers where the servers are numbered sequentially
starting from 1. Over time, any given server might explode, in which case its
server number is made available for reuse. When a new server is launched, it
should be given the lowest available number.

Write a function which, given the list of currently allocated server numbers,
returns the number of the next server to allocate. In addition, you should
demonstrate your approach to testing that your function is correct. You may
choose to use an existing testing library for your language if you choose, or
you may write your own process if you prefer.

For example, your function should behave something like the following:

  >> next_server_number([5, 3, 1])
  2
  >> next_server_number([5, 4, 1, 2])
  3
  >> next_server_number([3, 2, 1])
  4
  >> next_server_number([2, 3])
  1
  >> next_server_number([])
  1
'''


def next_server_number(ids):
    # Empty list?
    if not ids:
        return 1
    ids = sorted(ids)
    last_id = 0
    for _id in ids:
        if _id != last_id + 1:
            return last_id + 1
        last_id = _id
    return ids[-1] + 1


'''
Server names consist of an alphabetic host type (e.g. "apibox") concatenated
with the server number, with server numbers allocated as before (so "apibox1",
"apibox2", etc. are valid hostnames).

Write a name tracking class with two operations, allocate(host_type) and
deallocate(hostname). The former should reserve and return the next available
hostname, while the latter should release that hostname back into the pool.

For example:

>> tracker = Tracker.new()
>> tracker.allocate("apibox")
"apibox1"
>> tracker.allocate("apibox")
"apibox2"
>> tracker.deallocate("apibox1")
nil
>> tracker.allocate("apibox")
"apibox1"
>> tracker.allocate("sitebox")
"sitebox1"
'''


class Tracker(object):

    def __init__(self):
        self.type_to_ids = defaultdict(list)
        self.host_re = re.compile('^([A-z]+)(\d+)$')

    def allocate(self, host_type):
        next_id = next_server_number(self.type_to_ids[host_type])
        self.type_to_ids[host_type].append(next_id)
        return '%s%d' % (host_type, next_id)

    def deallocate(self, hostname):
        m = self.host_re.match(hostname)
        assert m
        host_type = m.group(1)
        id_ = int(m.group(2))
        self.type_to_ids[host_type].remove(id_)
