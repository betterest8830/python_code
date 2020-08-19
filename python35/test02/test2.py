# coding=utf8

def student_rank(data):
    result = {}
    for key, values in data.items():
        tmp =sorted(values.items(), key=lambda x: x[1], reverse=True)
        names = [a for (a, b) in tmp]
        scores = [b for (a, b) in tmp]
        print(scores)
        ranks = [1] * len(scores)
        for i in range(1, len(scores)):
            if scores[i] == scores[i-1]:
                ranks[i] = ranks[i-1]
            else:
                ranks[i] = i+1
        result = {}
        for i in range(len(names)):
            result[names[i]] = ranks[i]
        print(result)
    return result


student_rank({"class1": {"student1": 87, "student2": 98, "student3": 90},
              "class2": {"student1": 76, "student2": 97, "student3": 97}})

