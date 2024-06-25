from django.shortcuts import render
from .models import Post,Tag, Comments, Profile, WebsiteMeta
from .forms import CommentForm,SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.
def post_page(request, slug):
    form = CommentForm()

    if request.POST: 
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id = post_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                comment_reply = comment_form.save(commit=False)
                comment_reply.post = post
                comment_reply.parent = parent_obj
                comment_reply.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))
            else:
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))
    else:
        post = Post.objects.get(slug=slug)

    if post.view_count:post.view_count += 1
    else:post.view_count = 1
    post.save()

    comments = Comments.objects.filter(post=post, parent=None)
    context = {'post':post, 'form':form, 'comments' : comments}
    return render(request, 'app/post.html', context)

def index(request):
    top_post = Post.objects.all().order_by('-view_count')[:3]
    recent_post = Post.objects.all().order_by('-last_updated')[:3] 
    featured_post = Post.objects.filter(is_featured = True)
    if featured_post:
        featured_post = featured_post[0]
    subscribe_form = SubscribeForm()
    subscribe_successful = None

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid:
            subscribe_form.save()
            subscribe_successful = 'Subscribe Successfully'
            subscribe_form = SubscribeForm()

    website_info =  None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {
        'website_info' : website_info,
        'top_post' : top_post,
        'recent_post' : recent_post,
        'featured_post' : featured_post,
        'subscribe_form' : subscribe_form,
        'subscribe_successful': subscribe_successful
    }
    return render(request, 'app/index.html', context)

def tag(request, slug):
    tag = Tag.objects.get(slug = slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')
    if top_posts:top_posts[:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')
    if recent_posts:recent_posts[:3]
    featured_posts = Post.objects.filter(is_featured = True)
    if featured_posts:featured_posts[:3]
    context = {
        'tag':tag,
        'tags':Tag.objects.all(),
        'top_posts' : top_posts,
        'recent_posts' : recent_posts,
        'featured_posts' : featured_posts
    }
    return render(request, 'app/tag.html', context)

def author(request, slug):
    author = Profile.objects.get(slug = slug)
    top_posts = Post.objects.filter(author=author.user).order_by('-view_count')
    if top_posts:top_posts[:2]
    recent_posts = Post.objects.filter(author=author.user).order_by('-last_updated')
    if recent_posts:recent_posts[:3]
    featured_posts = Post.objects.filter(is_featured = True)
    if featured_posts:featured_posts[:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')
    if top_authors:top_authors[:10]
    context = {
        'author' : author,
        'top_authors' : top_authors,
        'top_posts' : top_posts,
        'recent_posts' : recent_posts,
        'featured_posts' : featured_posts
    }
    return render(request, 'app/author.html', context)

def search_posts(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    context = {
        'posts' : posts,
        'search_query' : search_query,
    }
    return render(request, 'app/search.html', context)

def all_post(request):
    context = {
        'data' : 1,
    }
    return render(request, 'app/all_post.html', context)

def about(request):
    website_info =  None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {
        'website_info' : website_info,
    }
    return render(request, 'app/about.html', context)

def contact_us(request):
    context = {
        'data' : 1,
    }
    return render(request, 'app/contact_us.html', context)
