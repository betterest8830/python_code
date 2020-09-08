# coding=utf8

import time


def log_time(throw_error):
    def decorater(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            time.sleep(1)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if throw_error:
                    raise e
            finally:
                print('run_time %s' % (time.time() - start))
        return wrapper
    return decorater
@log_time(throw_error=True)
def test(a, b):
    return a / b

print(test(10, 3))
#test(10, b=0)





'''
Group:
id, name 

Members:
gid, pername



Operation:
id, name, pid
1, modify, 1
2，，1

Permission:
id, name, gids 
1, 修改权限，[1,2]
2、读取权限，【1，2，3】

'''


