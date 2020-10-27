# coding=utf8


# 链表
class ListNode:
    def __init__(self,  val):
        self.next = None
        self.val = val
def gen_list():
    a, b, c, d = ListNode(1), ListNode(2), ListNode(3), ListNode(4)
    a.next = b
    b.next = c
    c.next = d


# 二叉树
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
def gen_tree():
    a, b, c, d, e, f, g = TreeNode(1), TreeNode(2), TreeNode(3), TreeNode(4), TreeNode(5), TreeNode(6), TreeNode(7)
    a.left = b
    a.right = c
    b.left = d
    b.right = e
    c.left = f
    c.right = g
    return a