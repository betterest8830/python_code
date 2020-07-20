# coding=utf


class ListNode(object):
    def __init__(self, n , v):
        self.next = n
        self.val = v

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


def find_num(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = low + (high-low) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] <= nums[high]:
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1
        else:
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
    return -1


def find_Kth(a, b, k):
    if not a: return b[k]
    if not b: return a[k]
    ia, ib = len(a) // 2, len(b) // 2
    va, vb = a[ia], b[ib]
    if ia + ib < k:
        if va < vb:
            find_Kth(a[ia+1:], b, k - (ia+1))
        else:
            find_Kth(a, b[ib+1:], k - (ib + 1))
    else:
        if va < vb:
            find_Kth(a, b[:ib], k)
        else:
            find_Kth(a[:ia], b, k)

def get_middle(nums1, nums2):
    length = len(nums1) + len(nums2)
    if length % 2:
        return find_Kth(nums1, nums2, length // 2)
    else:
        return (find_Kth(nums1, nums2, length // 2) + find_Kth(nums1, nums2, (length-1) // 2)) / 2
