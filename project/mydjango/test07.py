# coding=utf8


def min_jump(nums):
    step = 0
    cur_end, max_end = 0, 0
    for i, num in enumerate(nums):
        if i == cur_end + 1:
            cur_end = max_end
            step += 1
        max_end = max(max_end, i + num)
    return step


nums = [2, 3, 1, 1, 4]
print(min_jump(nums))