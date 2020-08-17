# coding=utf8


def count_arr(nums, n):
    i = 0
    while i < n:
        tmp = nums[i] - 1
        if tmp < 0:
            i += 1
            continue
        if nums[tmp] > 0:
            nums[i] = nums[tmp]
            nums[tmp] = -1
        else:
            nums[tmp] -= 1
            nums[i] = 0


def test():
    nums = [2, 5, 5, 2, 3]
    count_arr(nums, 5)
    print(nums)


test()