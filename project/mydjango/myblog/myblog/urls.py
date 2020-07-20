"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import blog.views as bv


# 配置url
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # 上面注释第一种：参数：URL正则、对应方法、名称
    url(r'^index/$', bv.index),
    # 上面注释最后一种
    #url(r'^blog/', include('blog.urls')),  # 总路径，app url 在其后面
    url(r'^blog/', include('blog.urls',  namespace='blog')),
]
