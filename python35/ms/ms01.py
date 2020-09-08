# coding=utf8


def student_rank(nums):
    for class_name, score_info in nums.items():
        tmp = sorted(score_info.items(), key=lambda x: x[1], reverse=True)
        print(tmp)
        cur_name, cur_score, cur_rank = tmp[0][0], tmp[0][1], 1
        res_d = {cur_name: cur_rank}
        for i, (name, score) in enumerate(tmp[1:], 2):
            if score != cur_score:
                cur_rank = i
            res_d[name] = cur_rank
        print(res_d)


student_rank({"class1": {"student1": 87, "student2": 98, "student3": 90},
              "class2": {"student1": 76, "student2": 97, "student3": 97}})

