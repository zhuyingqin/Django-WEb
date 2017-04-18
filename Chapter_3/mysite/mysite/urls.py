"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import  include, url 
from django.contrib import admin
# 站点地图导入的模块
from django.contrib.sitemaps.views import sitemap   #导入djangon内部站点地图函数函数
from blog.sitemaps import PostSitemap           # 导入blog下的所创建站点地图模块下的站点类 

sitemaps = { 'posts': PostSitemap, }             # 将站点地图获取的内容以字典的形式存储在变量sitemaps中
 
urlpatterns = [
	#主应用下的url
	url(r'^admin/', admin.site.urls),
	#主应用下的url
	url(r'^blog/', include('blog.urls',namespace='blog', app_name='blog')),
	#将blog中的URL模式包含到项目的主URL模式中,告诉Django在blog/路径下包含了blog应用中的urls.py定义的URL模式。你可以给它们一个命名空间叫做blog，这样你可以方便的引用这个URLs组
    url(r'^sitemap\.xml$', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #定义了一个URL模式来匹配sitemap.xml并使用sitemap视图（view），sitemaps字典会被传入到sitemap视图（view）中
]
 
 
