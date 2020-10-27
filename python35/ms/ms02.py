# coding=utf


class ListNode:
    def __init__(self,  val):
        self.next = None
        self.val = val

def gen_list():
    a, b, c, d = ListNode(1), ListNode(2), ListNode(3), ListNode(4)
    a.next = b
    b.next = c
    c.next = d


# 142. 环形链表 II
def is_cycle_list(head):
    if not head: return False
    start = slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            while start != slow:
                start = start.next
                slow = slow.next
            return start
    return False


# 206. 反转链表
def reverse_list(head):
    pre, cur = None, head
    while cur:
        cur.next, pre, cur = pre, cur, cur.next
    return pre


