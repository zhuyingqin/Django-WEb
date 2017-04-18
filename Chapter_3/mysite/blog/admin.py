from django.contrib import admin  
from .models import Post,  Comment            #为应用下的模型创建管理站点，导入模块下的Post，Comment

class PostAdmin(admin.ModelAdmin):
	#使用继承了ModelAdmin的定制类来告诉Django管理站点中需要注册我们自己的模型（model）。
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    #list_display属性允许设置一些想要在管理对象列表页面显示的模型（model）字段。
    list_filter = ('status', 'created', 'publish', 'author')
    #根据list_filter属性中指定的字段在右侧边栏过滤返回结果
    search_fields = ('title', 'body')
    #通过使用search_fields属性定义了一个搜索字段列
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    #通过定义date_hierarchy属性,实现可以通过时间层快速导航的栏
    ordering = ['status', 'publish']
    #该属性通过Status和Publish列进行排序


class CommentAdmin(admin.ModelAdmin):
	#添加新的模型（model）到管理站点中并通过简单的接口来管理评论。
    list_display = ('name', 'email', 'post', 'created', 'active')
    #定义显示属性的内容包含的内容
    list_filter = ('active', 'created', 'updated')
    #list_filter属性，实现简单的过滤功能
    search_fields = ('name', 'email', 'body')
    #通过使用search_fields属性定义了一个搜索字段列


admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)	
