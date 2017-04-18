#coding=utf-8
from django import forms           # 导入django内部表单功能
from .models import Comment        # 导入模型下的Comment


class EmailPostForm(forms.Form):
	#新建一个类用来实现Email 分享功能。该类继承forms类
    name = forms.CharField(max_length=25)
    # 定义name属性，使用CharField字段验证，这种类型的字段被渲染成<input type=“text”>HTML元素,参数用来控制最大输入长度
    email = forms.EmailField()
    '''
	email和to字段是EmailField,这两个字段都需要一个有效的email地址，否则字段验证将会抛出一
	个forms.ValidationError异常导致表单验证不通过。
    '''
    to = forms.EmailField()
    # 创建to的属性，生成一个表单，记录发给人的email.
    comments = forms.CharField(required=False,
                                         widget=forms.Textarea)
    #该属性，定义了在HTML元素中使用<textarea></textarea>，设置参数required=False让comments的字段可选


class CommentForm(forms.ModelForm):
	#使用ModelForm构建一个表单让用户在blog帖子下进行评论
    class Meta:
        model = Comment
        #需要在这个表单的Meta类里表明使用哪个模型（model）来构建表单。这里是Comment
        fields = ('name', 'email', 'body')
        # fields属性 定义了需要构建表单的对象。使用元组的方式


class SearchForm(forms.Form):
	#创建一个搜索表单用来实现输入框
	query= forms.CharField(label='输入关键字')
	#query属性，定义输入的字段，让用户引入搜索条件（terms）