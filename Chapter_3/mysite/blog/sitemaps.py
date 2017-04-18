from django.contrib.sitemaps import Sitemap   #继承sitemaps模块提供的Sitemap类用来创建一个自定义的站点地图
from .models import Post                      #关联模型下的Post模块

class PostSitemap(Sitemap):
	#创建一个类实现站点地图（sitemap），帮助网络爬虫（crawlers）来对你的网站内容进行索引和标记。
    changefreq = 'weekly'
    #定义属性表明了帖子页面修改的频率
    priority = 0.9
    # 该属性表明它们在网站中的关联性（暂时不懂何为关联性），最大值为1
    def items(self):
    	#定义方法属性
        return Post.published.all()
        #返回了在这个站点地图（sitemap）中所包含对象的查询集（QuerySet）
    def lastmod(self, obj):
    	# 定义另一个方法属性
        return obj.publish
        #用来接收items获取的对象集，返回对象的最后修改时间。