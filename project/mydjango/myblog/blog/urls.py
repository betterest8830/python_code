
from django.conf.urls import url
from . import views

# 新建的urls.py文件
# 配置url
urlpatterns = [
    url(r'^index/$', views.index),
    # url(r'^index$', views.index), # 结尾习惯性加上/
    # url(r'^$', views.index),
    # url(r'', views.index), 不严谨
    # 匹配到的的数字以article_id作为组名传递，与参数名一致
    # url(r'^article/(?P<article_id>[0-9]+)$', views.article_page),
    url(r'^article/(?P<article_id>[0-9]+)$', views.article_page, name='article_page'),
    # url(r'^edit/$', views.edit_page, name='edit_page'),
    url(r'^edit/(?P<article_id>[0-9]+)$', views.edit_page, name='edit_page'),
    url(r'^edit/action/$', views.edit_action, name='edit_action'),
]