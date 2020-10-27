# coding=utf8


# 33. 搜索旋转排序数组
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


# 4. 寻找两个正序数组的中位数
def get_middle(nums1, nums2):
    length = len(nums1) + len(nums2)
    if length % 2:
        return find_small_kth(nums1, nums2, length // 2)
    else:
        return (find_small_kth(nums1, nums2, length // 2) + find_small_kth(nums1, nums2, (length-1) // 2)) / 2
def find_small_kth(a, b, k):
    if not a: return b[k]
    if not b: return a[k]
    ia, ib = len(a) // 2, len(b) // 2
    va, vb = a[ia], b[ib]
    if ia + ib < k:
        if va < vb:
            find_small_kth(a[ia+1:], b, k - (ia+1))
        else:
            find_small_kth(a, b[ib+1:], k - (ib + 1))
    else:
        if va < vb:
            find_small_kth(a, b[:ib], k)
        else:
            find_small_kth(a[:ia], b, k)

# 45. 跳跃游戏 II
def min_jump(nums):
    step = 0
    cur_end, max_end = 0, 0
    for i, num in enumerate(nums):
        if i == cur_end + 1:
            cur_end = max_end
            step += 1
        max_end = max(max_end, i + num)
    return step
