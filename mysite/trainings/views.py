from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Language,Topic,Post,Feedback
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewTopicForm,NewPostForm,CommentForm,FeedbackForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg
from django.views.generic import UpdateView, ListView
import operator
from functools import reduce

def getLangList():
    latest_language_list = Language.objects.all()
    return latest_language_list

def index(request):
    language_list = getLangList()
    posts = Post.objects.all()
    latest_posts = posts.order_by('-posted_on')[0:3]
    popular_posts = posts.order_by('-views')[0:3]
    context = {
        'language_list': language_list,
        'latest_posts':latest_posts,
        'popular_posts':popular_posts,

    }
    return render(request, 'trainings/index.html',context)

@login_required
def topics(request,language_id):
    language = get_object_or_404(Language,pk=language_id)
    language_list = getLangList()
    context = {
        'language_list':language_list,
        'language':language,
    }
    return render(request,'trainings/topics.html',context)

@login_required
def posts(request,language_id,topic_id):
    topic = get_object_or_404(Topic,pk=topic_id)
    language_list = getLangList()
    latest_posts = topic.posts.order_by('-posted_on')
    popular_posts = topic.posts.order_by('-views')

    context = {
        'language_list':language_list,
        'topic':topic,
        'latest_posts':latest_posts,
        'popular_posts':popular_posts,
    }
    return render(request,'trainings/posts.html',context)

# class PostView(ListView):
#     model= Topic
#     context_object_name = 'topic'
#     template_name = 'trainings/posts.html'
#     paginate_by =3

#     def get_context_data(self, **kwargs):
#         context = super(PostView,self).get_context_data(**kwargs)
#         topic = get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))
#         context.update({
#             'language_list' : topic.posts.languages.all(),
#             'latest_posts' : topic.posts.order_by('-posted_on'),
#             'popular_posts' : topic.posts.order_by('-views'),
#         })
#     def get_queryset(self):
#         self.topic = get_object_or_404(Topic, pk=self.kwargs.get('topic_id'))
#         queryset = self.topic.posts.order_by('-posted_on')
#         return queryset

@login_required
def new_topic(request, language_id):
    language =get_object_or_404(Language,pk=language_id)
    language_list = getLangList()
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.language=language
            topic.save()
            return redirect('topics',language_id =language.id)
    else:
        form = NewTopicForm()
    context = {
        'language_list':language_list,
        'language':language,
        'form':form,
    }
    return render(request, 'trainings/new_topic.html',context)

@login_required
def new_post(request,language_id,topic_id):
    topic = get_object_or_404(Topic,pk=topic_id)
    language_list = getLangList()
    
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.posted_by = request.user
            post.save()
            return redirect('posts',language_id =language_id,topic_id=topic_id)
    else:
        form = NewPostForm()
    context = {
        'language_list':language_list,
        'topic':topic,
        'form':form,
    }
    return render(request, 'trainings/new_post.html',context)

@login_required
def visit_post(request,language_id,topic_id,post_id):
    post =get_object_or_404(Post,pk=post_id)
    language_list = getLangList

    feedback_post = Feedback.objects.filter(rated_post=post)
    avg_rating = feedback_post.aggregate(Avg('rating'))

    session_key = 'viewed_post_{}'.format(post.pk)
    if not request.session.get(session_key, False):
        post.views +=1
        post.save()
        request.session[session_key] = True        

    context = {
        'language_list':language_list,
        'post':post,
        'avg_rating':avg_rating,
    }

    return render(request, 'trainings/visit_post.html',context)

@login_required
def search(request):
    language_list = getLangList()
    posts = Post.objects.all()

    query = request.GET.get('q')
    if query:
        query_list = query.split()
        search_posts = posts.filter(
            reduce(operator.and_,
            (Q(title__icontains=q)for q in query_list))|
            reduce(operator .and_,
            (Q(description__icontains=q)for q in query_list))
        )
    else:
        search_posts = posts
    context = {
        'language_list':language_list,
        'search_posts':search_posts,
    }

    return render(request,'trainings/search.html',context)

@login_required
def my_account(request):
    language_list =getLangList()
    posts = Post.objects.all()
    my_posts = posts.filter(posted_by=request.user)
    latest_posts = my_posts.order_by('-posted_on')
    popular_posts = my_posts.order_by('-views')
    context ={
        'language_list':language_list,
        'my_posts':my_posts,
        'latest_posts':latest_posts,
        'popular_posts':popular_posts,
    }
    return render(request,'trainings/my_account.html',context)

@login_required
def new_comment(request,language_id,topic_id,post_id):
    post =get_object_or_404(Post,pk=post_id)
    language_list = getLangList
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.commented_by=request.user
            comment.save()
            return redirect('visit_post',language_id =language_id,topic_id=topic_id,post_id=post_id)
    else:
        form =CommentForm()
    context = {
        'language_list':language_list,
        'post':post,
        'form':form,
    }
    return render(request,'trainings/comment_post.html',context)

@login_required
def feedback_post(request,language_id,topic_id,post_id):
    post =get_object_or_404(Post,pk=post_id)
    language_list = getLangList

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.rating = request.POST.get('rating')
            feedback.rated_by = request.user
            feedback.rated_post = post
            feedback.save()
            return redirect('visit_post',language_id =language_id,topic_id=topic_id,post_id=post_id)
    else:
        form =FeedbackForm()
    context = {
        'language_list':language_list,
        'post':post,
        'form':form,
    }
    return render(request,'trainings/submit_feedback.html',context)

