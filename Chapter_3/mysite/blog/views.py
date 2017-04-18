#coding=utf-8
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render ,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger   # 导入内置的Paginator类允许你方便的管理分页
from django.views.generic import ListView                             	   # 通过使用Django提供的通用ListView使我们的post_list视图（view）转变为一个基于类的视图。
from .models import Post ,Comment
from .forms import EmailPostForm , CommentForm ,SearchForm	               # 导入表单下创建的邮件分享功能的EmailPostForm表单,用户评论功能的表单,搜索引擎表单进行关联 				
from django.core.mail import send_mail                                     # 导入邮件发送功能模块
from django.db.models import Count                                         # 导入Django ORM的Count聚合函数
from haystack.query import SearchQuerySet                                  # 导入haystack应用下搜索查询集函数
from taggit.models import Tag                                              # django-taggit中导入Tag模型（model）


def post_list(request, tag_slug=None):
	#创建第一个Django视图（view），用来展示帖子的列表,和标签,参数会带进url
	object_list = Post.published.all()
	#构建查询集获取所有状态为已发布的帖子通过使用我们之前创建的published管理器（manager）。
	tag = None

	if tag_slug:
		#假如给予一个标签 slug
		tag = get_object_or_404(Tag, slug=tag_slug)
		# 通过get_object_or_404()用给定的slug来获取标签对象。
		object_list = object_list.filter(tags__in=[tag])  
		'''滤所有帖子只留下包含给定标签的帖子，因为有一个多对多（many-to-many）的关系，
		   必须通过给定的标签列表来过滤，标签列表只包含一个元素。'''
	paginator = Paginator(object_list, 3)
	# 设定变量，每页最多显示三个对象列表
	
	page = request.GET.get('page')
	#获取到page GET参数来指明页数
	try:
		#异常判断
		posts = paginator.page(page)
		#通过调用Paginator的 page()方法在期望的页面中获得了对象
	except PageNotAnInteger:
		# 如果page参数不是一个整数，
		posts = paginator.page(1)
		#我们就返回第一页的结果。我们就展示最后一页的结果。
	except EmptyPage:
		#如果这个参数数字超出了最大的页数，
		posts = paginator.page(paginator.num_pages)
        #展示最后一页的结果。
		

	return render(request, 
    			'blog/post/list.html', 
    			{'page': page,
    			'posts': posts,
    			'tag': tag})
    # 返回请求，模板（templates）下list.html的网页内容，以及所有的posts内容。


class PostListView(ListView):
	#创建视图，基础视图（view）允许你对任意的对象进行排列。
    queryset = Post.published.all()
    #特定的查询集（QuerySet）代替取回所有的对象。
    context_object_name = 'posts'
    #使用环境变量posts给查询结果，默认是post_list视图中的object_list
    paginate_by = 3
    #结果进行分页处理每页只显示3个对象。
    template_name = 'blog/post/list.html'
    #使用定制的模板（template）来渲染页面，默认的将是post_list视图对应的url---blog/post_list.html。    


def post_detail(request, year, month, day, post):
	'''创建第二个视图（view）来展示一篇单独的帖子,帖子包含用户评论的动态显示'''
	post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
	#使用year，month，day以及post作为参数通过给予slug和日期来获取到一篇已经发布的帖子

	comments = post.comments.filter(active=True)
	#添加了一个查询集（QuerySet）来获取这个帖子所有有效的评论，通过参数过滤所有已经发布过的
	new_comment = None
	# 定义一个变量名为new_comment 及为新的评论 为 空

	if request.method == 'POST':
		 # 如果是通过POST请求，我们使用提交的数据新建一条评论
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# 用is_valid()方法验证这些数据去实例化表单，如果表单通过验证，我们会做以下的操作：
			new_comment = comment_form.save(commit=False)
			'''
            通过调用表单的save()方法创建一个新的Comment对象，参数执行使对象无法立即保存到数据库中。
            注意save()方法是给ModelForm用的，而不是给Form实例用的
            '''
			new_comment.post = post
			 #为刚创建的评论分配到当前的帖子
			new_comment.save()
			# 再次执行保存，这次是保存到数据库中的
	else:
		#通过GET请求被加载的，那么我们用comment_fomr = commentForm()来创建一个表单实例。
		comment_form = CommentForm()

	post_tag_ids = post.tags.values_list('id', flat=True)
	#取回了一个包含当前帖子所有标签的ID的Python列表,values_list() 查询集（QuerySet）返回包含给定的字段值的元组
	similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
	 #获取所有包含这些标签的帖子排除了当前的帖子.
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
	'''使用Count聚合函数来生成一个计算字段same_tags，该字段包含与查询到的所有标签共享的标签数量。
    通过共享的标签数量来排序（降序）结果并且通过publish字段来挑选拥有相同共享标签数量的帖子中的最近的一篇帖子。
    对返回的结果进行切片只保留最前面的4篇帖子。'''

	return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments': comments, 
                  'comment_form': comment_form,
                  'similar_posts': similar_posts})
    #使用render()快捷方法来使用一个模板（template）去渲染取回的帖子。


def post_share(request, post_id):
    # 定义了post_share视图，参数为request对象和post_id
    post = get_object_or_404(Post, id=post_id, status='published')
    #使用get_object_or_404快捷方法通过ID获取对应的帖子,并且确认获取帖子的状态是'published'
    sent = False
    if request.method == 'POST':
        # 使用POST请求新建一个表单。
        form = EmailPostForm(request.POST)
        # 设定一个form变量用来存储提交的表单
        if form.is_valid():
        	# 如果提交的表单，有效（非空，等其他限制要求），返回一个True,则执行后续操作
            cd = form.cleaned_data
            # 如果表单数据验证通过，通过访问form.cleaned_data获取验证过的数据赋值给变量cd。这个属性是一个表单字段和值的字典。
            post_url = request.build_absolute_uri(
                                    post.get_absolute_url())
            '''
			新建分享表单成功后，将会在模板中使用这个变量显示一条成功提示，由于需要在email中包含具体帖子的链接，所以通过使用
			post.get_absolute_url()方法来获取到帖子的绝对路径。将这个绝对路径作为request.build_absolute_uri()的输入值来构建
			一个完整的包含了HTTP 概要和主机名的URL
            '''
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            #设置一个变量subject用来存储一条消息，消息内容通过使用字符串格式化将新建表单的name,email地址，帖子主题传递到消息中。
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            #设置一个变量message用来接收一条消息，消息使用字符串格式化，将选择分享表单的主题，url名字，以及新建表单的内容（表单comments属性）
            #send_mail(subject, message, [cd['email']], [cd['to']])
            sent = True
            #声明了一个sent变量并且当帖子被成功发送时赋予它True。
    else:
        form = EmailPostForm()
        #如果请求方式是GET，即直接获取已经分享过帖子
    return render(request, 'blog/post/share.html', {'post': post, 
    												'form': form,
    												'sent': sent})
    # 最终返回展示内容：templates对应的模板，分享的帖子，评论。

def post_search(request):
    #新建函数定义帖子搜索视图
    form = SearchForm()
    #变量form实例化创建的SearchForm表单.
    context = {'form': form }
    # 将实例化表单以字典的形式存入变量context中
    if 'query' in request.GET:
        '''
        使用GET方法来提交这个表单（form）可以直接在url上输入查询字段。
        假设这个表单（form）已经被提交，我们将在request.GET字典中查找query参数
        '''
        form = SearchForm(request.GET)
        #表单（form）被提交后，我们通过提交的GET数据来实例化它，  
        if form.is_valid():
        #如果这个表单有效
            cd = form.cleaned_data
            # 将表单(form)返回的值以字典的形式存储在变量cd中
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            '''
            使用earchQuerySet为所有被编入索引的并且主要内容中包含给予的查询内容的Post对象来执行一次搜索
            load_all()方法会立刻加载所有在数据库中有关联的Post对象
            '''
            total_results = results.count()
            # 将查询到的的对象总数赋值给变量total_results
            
            context.update({ 'cd':cd, 
                     'results': results,
                     'total_results':
                      total_results})
            #使用update方法将本地变量（cd,results）结果及查询到的总数追加到变量context中。
    return render(request, 'blog/post/search.html', context)
    # 返回请求，渲染模板，将变量内容传入模板中