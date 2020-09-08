# coding=utf8


class ThreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.mid = None


class TreeNode(object):
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


def is_symmetrical(root):
    def is_sym(p, q):
        if p and q:
            return p.val == q.val and is_sym(p.left, q.right) and is_sym(p.right, q.left)
        return p == q
    if not root: return False
    return is_sym(root.left, root.right)


def is_symmetrical2(root):
    level = [(root, root)]
    while level:
        left, right = level.pop(0)
        if not left and not right:
            continue
        if not left or not right:
            return False
        if left.val != right.val:
            return False
        level.append((left.left, right.right))
        level.append((left.right, right.left))
    return True


def is_symmetrical3(root):
    pass


