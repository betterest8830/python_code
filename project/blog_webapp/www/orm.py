# !/usr/bin/env python3
# -*- coding=utf8 -*-

__author__ = 'xcl'


import aiomysql # 异步mysql驱动支持
import logging
logging.basicConfig(level=logging.INFO)


def log(sql, args=()):
    logging.info('SQL: %s' % sql)

# 该函数用于创建连接池
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        # 数据库名字，如果做ORM测试的使用请使用db=kw['db']
        #db=kw['db'], # 测试使用
        db=kw['database'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        # 连接池最多同时处理10个请求
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        # 传递消息循环对象loop用于异步执行
        loop=loop
    )

# =============================SQL处理函数区==========================
# select和execute方法是实现其他Model类中SQL语句都经常要用的方法，原本是全局函数，这里作为静态函数处理

# select语句则对应该select方法,传入sql语句和参数
async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs

# execute方法只返回结果数，不返回结果集,用于insert,update这些SQL语句
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

# ========================================Model基类以及具其元类=====================
# 对象和关系之间要映射起来，首先考虑创建所有Model类的一个父类，
# 具体的Model对象（就是数据库表在你代码中对应的对象）再继承这个基类
class ModelMetaclass(type):
    '''
    该元类主要使得Model基类具备以下功能:
    1.任何继承自Model的类（比如User），会自动通过ModelMetaclass扫描映射关系
    并存储到自身的类属性如__table__、__mappings__中
    2.创建了一些默认的SQL语句
    '''
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table名称,一般就是Model类的类名:
        tableName = attrs.get('__table__', None) or name
        logging.info('found model:%s (table:%s)' % (name, tableName))
        # 获取所有的Field和主键名
        mappings = dict()
        primaryKey = None
        fields = []
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('found mapping: %s ==> %s' % (k, v))
                # k,v键值对全部保存到mappings中，包括主键和非主键。
                mappings[k] = v
                if v.primary_key:
                    #  如果primaryKey属性已经不为空了，说明已经有主键了，则抛出错误,因为只能1个主键
                    if primaryKey:
                        # python3中StandardError已经被取消了，使用Exception取代。
                        raise Exception('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    # 非主键全部放到fields列表中
                    fields.append(k)
        if not primaryKey:
            raise Exception('Primary key not found.')
        # 清除mappings，防止实例属性覆盖类的同名属性，造成运行时错误
        for k in mappings.keys():
            # attrs中对应的属性则需要删除。
            attrs.pop(k)

        # %s占位符全部替换成具体的属性名
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        # ===========初始化私有私有的特别属性===========
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        # ===========构造默认的select,insert,update,delete语句=======
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        # 第三个占位符有很多问号，为了方便就直接使用了create_ars_string函数来生成num个占位符的string
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
        tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
        tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

class Model(dict, metaclass=ModelMetaclass):
    '''
    继承dict是为了使用方便，例如对象实例user['id']即可轻松通过UserModel去数据库获取到id
    元类自然是为了封装我们之前写的具体的SQL处理函数，从数据库获取数据
    '''
    def __init__(self, **kw):
        super().__init__(**kw)
    # 调用不存在的属性时返回一些内容
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
    # 获取某个具体的值，肯定存在的情况下使用该函数,否则会使用__getattr()__
    def getValue(self, key):
        return getattr(self, key, None)
    # 不是很明白
    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    # --------------------------每个Model类的子类实例应该具备的执行SQL的方法比如save------
    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause.'
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        print(' '.join(sql))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    # 获取行数
    # 这里的 _num_ 什么意思？别名？ 我估计是mysql里面一个记录实时查询结果条数的变量
    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s as _num_ from `%s`' % (selectField, cls.__table__)]
        print(sql)
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        print(rs)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    # 根据主键查找
    # pk是主键
    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    # 这个是实例方法
    # argS是保存所有Model实例属性和主键的list,使用getValueOrDefault方法的好处是保存默认值
    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warnning('failed to insert record: affected rows: %s' % rows)

    # 这里使用getValue说明只能更新那些已经存在的值，因此不能使用getValueOrDefault方法
    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warning('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        print(args)
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warning('failed to remove by primary key: affected rows: %s' % rows)


# =====================================属性类===============================
# 属性的基类，给其他具体Model类继承
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        # 如果存在default，在getValueOrDefault中会被用到
        self.default = default
    # 直接print的时候定制输出信息为类名和列类型和列名
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)
class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)
class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)
class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)
class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)
