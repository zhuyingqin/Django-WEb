from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  #关联上Django权限系统的User模型（model）。
from django.core.urlresolvers import reverse   # 导入reverse()方法，通过它们的名字和可选的参数来构建URLS
from taggit.managers import TaggableManager    #添加django-taggit提供的TaggableManager管理器（manager）


class PublishedManager(models.Manager):
	#为模型（models）添加管理器（managers）：
    def get_queryset(self):
    	#get_queryset()是返回执行过的查询集（QuerySet）的方法属性
        return super(PublishedManager, self).get_queryset()\
                .filter(status='published')
        # 返回


class Post(models.Model):                  #新建一个类用来定义贴子的模型
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)  #title属性对应帖子的标题。它是CharField，在SQL数据库中会被转化成VARCHAR。最长显示的字段为250
    '''author属性，定义帖子用户名。使用外键关联框架内部的指定的user账户，告诉Django一篇帖子只能由一名用户编写，
    一名用户能编写多篇帖子。根据这个字段，Django将会在数据库中通过有关联的模型（model）主键来创建一个外键。
    通过related_name属性指定了从User到Post的反向关系名。
    '''
    author = models.ForeignKey(User, related_name='blog_posts')
    '''
    slug属性定义帖子的短标签，标签只包含字母，数字，下划线或连接线。我们将通过使用slug
    字段给我们的blog帖子构建漂亮的，友好的URLs。unique_for_date参数，这样我们就可以使用日
    期和帖子的slug来为所有帖子构建URLs。在相同的日期中Django会阻止多篇帖子拥有相同的slug。
    '''
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # body属性，帖子的主体。它是TextField，在SQL数据库中被转化成TEXT。
    body = models.TextField()
    #表明帖子什么时间发布。使用Djnago的timezone的now方法来设定默认值。随系统时间。
    publish = models.DateTimeField(default=timezone.now)
    #表明帖子什么时间创建，使用auto_now_add，当一个对象被创建的时候这个字段会自动保存当前日期
    created = models.DateTimeField(auto_now_add=True)
    #表明帖子什么时候更新。使用了auto_now，当更新保存一个对象的时候这个字段将会自动更新到当前日期。
    updated = models.DateTimeField(auto_now=True)
    #表示当前帖子的展示状态。使用choices参数，这样这个字段的值只能是给予的选择参数中的某一个值。
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    tags = TaggableManager() 
    #新建一个属性用来定义一个标签管理器，给Post对象添加，获取以及移除标签

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
    	#模型（model）中的类Meta包含元数据
        ordering = ('-publish',)                 # 查询数据库的时候默认返回的是根据publish字段进行降序排列过的结果。使用负号来指定进行降序排列。


    def __str__(self):
    	#str()方法是当前对象默认的可读表现
        return self.title                      # 返回title内容。

    def get_absolute_url(self):
    	#添加get_absolute_url()方法用来返回一个对象的标准URL。
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                              self.publish.strftime('%m'),
                              self.publish.strftime('%d'),
                              self.slug])
        #使用reverse()方法允许你通过它们的名字和可选的参数来构建URLS


class Comment(models.Model):
	# 创建一个模型（model）来存储评论。
    post = models.ForeignKey(Post, related_name='comments')
    # post属性使用一个外键将一个单独的帖子和评论关联起来。
    name = models.CharField(max_length=80)
    # name属性用来 定义评论的名字，参数限定字符串长度
    email = models.EmailField()
    #email属性使用EmailField字段来定义
    body = models.TextField()
    #body属性定义评论的内容
    created = models.DateTimeField(auto_now_add=True)
    #created属性定义评论的时间
    updated = models.DateTimeField(auto_now=True)
    # updated属性定义更新时间
    active = models.BooleanField(default=True)
    # active属性通过BoolernField字段及参数确定是否提交评论

    class Meta:
    	#继承Meta
        ordering = ('created',)
        #对评论按照创建的时间排序

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
        #返回一行字符串