from django.contrib.syndication.views import Feed                        #导入syndication框架的Feed类，动态（dynamically）生成RSS或者Atom feeds。
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
	#继承syndication框架的Feed类创建了一个子类
    title = 'My blog'
    #定义一个属性用来显示 title
    link = '/blog/'
    #该属性对应模板中的<link>
    description = 'New posts of my blog.'
    #同上该属性为了对应templat中的 <description>

    def items(self):
    	#定义items()方法返回包含在feed中的对象
        return Post.published.all()[:5]
        #返回最新五个已发布的帖子，包含在feed对象中。

    def item_title(self, item):
    	#定义方法属性
        return item.title
        #从items方法获取的帖子中提取各自的主题

    def item_description(self, item):
    	#定义方法属性用来获取帖子描述信息
        return truncatewords(item.body, 30)
        #使用内置的truncatewords模板过滤器（template filter）构建帖子的描述信息并只保留最前面的30个单词。