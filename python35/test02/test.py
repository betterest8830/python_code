# coding=utf8

class Node(object):
	def __init__(self, value=None, left=None, right=None, mid=None):
		self.value = value
		self.left = left
		self.right = right
        self.mid = mid

def pre_revers(root):
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


def is_sym(p, q):
    if p and q:
        return p.val == q.val and is_sym(p.left, q.right) and is_sym(p.right, q.left)
    return p == q

def is_symtric(root):
    if not root: return False
    return is_sym(root.left, root.right)



def is_sym3(p, q):
    if p and q:
        return p.val == q.val \
               and is_sym3(p.left, q.right) \
               and is_sym3(p.right, q.left) \
               and is_sym3(p.mid, q.mid)
    return p == q

def is_symtric3(root):
    if not root: return False
    if not root.mid:
        return is_sym3(root.left, root.right)
    else:
        return is_sym3(root.left, root.right) and is_sym3(root.mid.left, root.mid.right)

