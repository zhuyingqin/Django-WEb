from django import template                          #将django内部模板template导入
from django.db.models import Count                   #导入数据库中Count聚合函数，进行聚合查询
from django.utils.safestring import mark_safe        # 导入django内部安全方法
import markdown                                      # 导入markdown应用，使帖子可以使用markdown语法


register = template.Library()
#register变量来表明自己是一个有效的标签（tag）库,是template.Library的一个实例

from ..models import Post     # 导入应用下模块种Post模型

@register.simple_tag #如果你想使用别的名字来注册这个标签（tag），你可以指定装饰器的name属性，比如@register.simple_tag(name='my_tag')
#用@register.simple-tag装饰器定义此函数为一个简单标签（tag）并注册它。 
def total_posts():
	#用一个Python函数定义了一个名为total_posts的标签，Django将会使用这个函数名作为标签（tag）名
    return Post.published.count()  #通过count方法，计数出状态为published帖子的数量。	


@register.inclusion_tag('blog/post/latest_posts.html')
#通过装饰器@register.inclusion_tag注册模板标签，指定模板必须被blog/post/latest_posts.html返回的值渲染。
def show_latest_posts(count=3):
	# 创建另外一个标签（tag），可以在blog的侧边栏（sidebar）展示最新的几个（默认是5）帖子。
    latest_posts = Post.published.order_by('-publish')[:count]
    #定义变量表示最新发布的帖子：使用order_by('-publish')[:count](按照发布时间倒序)查询的结果
    return {'latest_posts': latest_posts}
    #函数返回了包含标签（inclusion tags）的一个字典变量而不是一个简单的值。


@register.assignment_tag
#创建一个分配标签（assignment tag）来展示拥有最多评论的帖子
def get_most_commented_posts(count=3):
	#定义函数名用来展示评论最多的帖子，参数用来显示展示的数量，默认是5
    return Post.published.annotate(
                total_comments=Count('comments')
            ).order_by('-total_comments')[:count]
    '''
	使用annotate()函数构建查询集（QuerySet）统计出每一个帖子的评论总数并保存在total_comments字段中，
	通过这个字段对查询集（QuerySet）进行排序。还提供了一个可选的count变量，通过给定的值来限制返
	回的帖子数量
    '''

@register.filter(name='markdown')
#注册己的模板过滤器（template filter），过滤器（filter）命名为markdown
def markdown_format(text):
	#避免函数名和markdown模板名起冲突，将函数命名为markdown_format
    return mark_safe(markdown.markdown(text))
    '''使用Django提供的mark_safe方法来标记结果，在模板（template）中作为安全的HTML被渲染
    默认的，Django不会信赖任何HTML代码并且在输出之前会进行转义。唯一的例外就是被标记为安
    全转义的变量。这样的操作可以阻止Django从输出中执行潜在的危险的HTML，并且允许你创建一
    些例外情况只要你知道你正在运行的是安全的HTML。'''