# coding=utf8


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


# 144. 二叉树的前序遍历
def preorder_traverse(root):
    if not root: return
    res, stk, cur = [], [], root
    while stk or cur:
        if cur:
            stk.append(cur)
            res.append(cur.val)
            cur = cur.left
        else:
            cur = stk.pop()
            cur = cur.right
    return res


# 102. 二叉树的层序遍历
def level_tarverse(root):
    if not root: return []
    level, res, tmp = [root], [], []
    while level:
        res += [node.val for node in level][::-1]
        for node in level:
            if node.left: tmp.append(node.left)
            if node.right: tmp.append(node.right)
        level, tmp = tmp, []
    return res


# 101. 对称二叉树
def is_symmetrical(root):
    def is_sym(p, q):
        if p and q:
            return p.val == q.val and is_sym(p.left, q.right) and is_sym(p.right, q.left)
        return p == q
    if not root: return False
    return is_sym(root.left, root.right)



