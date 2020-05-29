#!/usr/bin/env python3
# coding=utf8

import logging
logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

import orm as orm
from web_frame import add_routes, add_static
from config import configs
from handlers import COOKIE_NAME, cookie2user


def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    # 初始化模板配置，包括模板运行代码的开始结束标识符，变量的开始结束标识符等
    options = dict(
        # 是否转义设置为True，就是在渲染模板时自动把变量中的<>&等字符转换为&lt;&gt;&amp;
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),  # 运行代码的开始标识符
        block_end_string=kw.get('block_end_string', '%}'),  # 运行代码的结束标识符
        variable_start_string=kw.get('variable_start_string', '{{'),  # 变量开始标识符
        variable_end_string=kw.get('variable_end_string', '}}'),  # 变量结束标识符
        # Jinja2会在使用Template时检查模板文件的状态，如果模板有修改， 则重新加载模板。如果对性能要求较高，可以将此值设为False
        auto_reload=kw.get('auto_reload', True)
    )
    # 从参数中获取path字段，即模板文件的位置
    path = kw.get('path', None)
    # 如果没有，则默认为当前文件目录下的 templates 目录
    if path is None:
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    # Environment是Jinja2中的一个核心类，它的实例用来保存配置、全局对象，以及从本地文件系统或其它位置加载模板。
    # 这里把要加载的模板和配置传给Environment，生成Environment实例
    env = Environment(loader=FileSystemLoader(path), **options)
    # 从参数取filter字段
    # filters: 一个字典描述的filters过滤器集合, 如果非模板被加载的时候, 可以安全的添加filters或移除较早的.
    filters = kw.get('filters', None)
    # 如果有传入的过滤器设置，则设置为env的过滤器集合
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    # 给webapp设置模板
    app['__templating__'] = env


# ------------------------------------------拦截器middlewares设置-------------------------

async def logger_factory(app, handler):
    # 在正式处理之前打印日志
    async def logger(request):
        logging.info('Requst : %s, %s' % (request.method, request.path))
        return (await handler(request))
    return logger

async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json : %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form : %s' % str(request.__data__))
        return (await handler(request))
    return parse_data

# 是为了验证当前的这个请求用户是否在登录状态下，或是否是伪造的sha1
async def auth_factory(app, handler):
    async def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        # 获取到cookie字符串
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            # 通过反向解析字符串和与数据库对比获取出user
            user = await cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                # user存在则绑定到request上，说明当前用户是合法的
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')
        # 执行下一步
        return (await handler(request))
    return auth

# 响应处理
# 总结下来一个请求在服务端收到后的方法调用顺序是:
#     	logger_factory->response_factory->RequestHandler().__call__->get或post->handler
# 那么结果处理的情况就是:
#     	由handler构造出要返回的具体对象
#     	然后在这个返回的对象上加上'__method__'和'__route__'属性，以标识别这个对象并使接下来的程序容易处理
#     	RequestHandler目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，调用URL函数,然后把结果返回给response_factory
#     	response_factory在拿到经过处理后的对象，经过一系列对象类型和格式的判断，构造出正确web.Response对象，以正确的方式返回给客户端
# 在这个过程中，我们只用关心我们的handler的处理就好了，其他的都走统一的通道，如果需要差异化处理，就在通道中选择适合的地方添加处理代码。
# 在response_factory中应用了jinja2来套用模板
async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        logging.info('r = %s' % str(r))
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False,
                    default=lambda o: o.__dict__).encode('utf8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                # 登录使用
                r['__user__'] = request.__user__
                resp = web.Response(body=app['__templating__'].
                                    get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(status=t, text=str(m))
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

'''
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')
@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv
'''

async def init(loop):
    await orm.create_pool(loop=loop, **configs.db)
    # await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='password', db='pure_blog')
    '''
    # middlewares设置两个中间处理函数
    # middlewares中的每个factory接受两个参数，app 和 handler(即middlewares中得下一个handler)
    # 譬如这里logger_factory的handler参数其实就是response_factory()
    # middlewares的最后一个元素的Handler会通过routes查找到相应的，其实就是routes注册的对应handler
    '''
    app = web.Application(loop=loop, middlewares=[logger_factory, auth_factory, response_factory])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    #add_routes(app, 'handlers_test')
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()