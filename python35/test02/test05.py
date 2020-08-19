# coding=utf8


def reverse_list(head):
    pre, cur = None, head
    while cur:
        cur.next, pre, cur = pre, cur, cur.next
    return pre

def level_order(root):
    if not root: return []
    level, res, tmp = [root], [], []
    while level:
        res += [node.val for node in level][::-1]
        for node in level:
            if node.left: tmp.append(node.left)
            if node.right: tmp.append(node.right)
        level, tmp = tmp, []
    return res


