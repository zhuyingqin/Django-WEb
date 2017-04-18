from haystack import indexes               #导入haystack下的indexex模块
from .models import Post                   #关联模型下的 Post，告诉django这是一个Post模型（model）的自定义SearchIndex。

class PostIndex(indexes.SearchIndex, indexes.Indexable):
	#创建一个为模型Post的索引类：是通过继承indexes.SearchIndex和indexes.Indexable构建的
    text = indexes.CharField(document=True, use_template=True)
    '''
    字段命名为text-是一个主要的搜索字段，通过使用use_template=True，告诉Haystack这
    个字段将会被渲染成一个模板（template）来构建document,它会被搜索引擎编入索引（index）
    '''
    publish = indexes.DateTimeField(model_attr='publish')
    #publish字段是一个日期字段也会被编入索引,通过model_attr参数来表明这个字段对应Post模型中的publish属性字段

    def get_model(self):
    	#定义get_model方法
        return Post
        #返回将储存在这个索引中的documents的模型（model）

    def index_queryset(self, using=None):
    	#定义index_queryset()方法
        return self.get_model().published.all()
        #返回将会被编入索引的对象的查询集（QuerySet）。这里只包含了发布状态的帖子。