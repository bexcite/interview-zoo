'''
Given a linked list, determine if it has a cycle in it.

Follow up:
Can you solve it without using extra space?
'''


class ListNode(object):
    '''
    Definition for singly-linked list.
    '''

    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):

    def hasCycle(self, head):
        """
        :type head: ListNode
        :rtype: bool
        """
        def safe_next(node):
            return node.next if node else None

        fast = safe_next(head)
        slow = head

        while not (fast is None or slow is None):
            if fast == slow:
                return True
            fast = safe_next(safe_next(fast))
            slow = safe_next(slow)

        return False
