# codiing=utf8

from models import User
import orm as orm
import asyncio, time


# 测试插入
async def test_save(loop):
    await orm.create_pool(loop, user='root', password='password', db='pure_blog')
    u = User(name='hi', email='hi@example.com', passwd='hi', image='about:blank')
    await u.save()

# 测试查询
async def test_findAll(loop):
    await orm.create_pool(loop, user='root', password='password', db='pure_blog')
    rs = await User.findAll(email='hi@example.com')
    for i in range(len(rs)):
        print(rs[i])

# 测试查询条数(不是)
async def test_findNumber(loop):
    await orm.create_pool(loop, user='root', password='password', db='pure_blog')
    count = await User.findNumber('email')
    print(count)

# 测试删除(主键)
async def test_remove(loop):
    await orm.create_pool(loop, user='root', password='password', db='pure_blog')
    u = User(id='0015900516512430ace0baa17fa4cc085f3c4069288c30a000')
    await u.remove()

# 测试更新(主键)
async def test_update(loop):
    await orm.create_pool(loop, user='root', password='password', db='pure_blog')
    # 必须按照列的顺序来初始化：'update `users` set `created_at`=?, `passwd`=?, `image`=?,
    # `admin`=?, `name`=?, `email`=? where `id`=?' 注意这里要使用time()方法，否则会直接返回个时间戳对象，而不是float值
    # id必须和数据库一直，其他属性可以设置成新的值,属性要全
    u = User(id='001590051680518bfd081525dbe427692e9fcc5e1a2dbe5000', created_at=time.time(), passwd='test',
             image='about:blank', admin=True, name='test', email='hello1@example.com')
    await u.update()

loop = asyncio.get_event_loop()
#loop.run_until_complete(test_save(loop))
#loop.run_until_complete(test_findAll(loop))
# loop.run_until_complete(test_findNumber(loop))
#loop.run_until_complete(test_remove(loop))
loop.run_until_complete(test_update(loop))
__pool = orm.__pool
__pool.close() # 需要先关闭连接池
loop.run_until_complete(__pool.wait_closed())
loop.close()

