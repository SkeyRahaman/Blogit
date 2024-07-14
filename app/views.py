from .models import Post, Tag, Comments, Profile, WebsiteMeta
from .forms import CommentForm, SubscribeForm, NewUserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth import login
from django.contrib.auth.models import User

# View for displaying a single post with comments and related information
def post_page(request, slug):
    form = CommentForm()

    # Handle POST request for comment submission
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post

            # Check if the comment is a reply to another comment
            parent_id = request.POST.get('parent')
            if parent_id:
                parent = get_object_or_404(Comments, id=parent_id)
                comment.parent = parent
            
            comment.save()
            return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    else:
        post = get_object_or_404(Post, slug=slug)

    # Increment view count
    post.view_count = post.view_count + 1 if post.view_count else 1
    post.save()

    # Retrieve comments, bookmark status, and like status
    comments = Comments.objects.filter(post=post, parent=None)
    is_bookmarked = post.bookmarks.filter(id=request.user.id).exists()
    liked = post.likes.filter(id=request.user.id).exists()
    total_likes = post.likes.count()

    # Retrieve side bar data
    recent_post = Post.objects.exclude(id=post.id).order_by('-last_updated')[:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')[:3]
    tags = Tag.objects.all()
    related_post = Post.objects.exclude(id=post.id).filter(author=post.author)[:3]

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
        'liked': liked,
        'total_likes': total_likes,
        'recent_post': recent_post,
        'top_authors': top_authors,
        'tags': tags,
        'related_post': related_post,
    }
    return render(request, 'app/post.html', context)

# View for displaying the index page
def index(request):
    top_post = Post.objects.all().order_by('-view_count')[:3]
    recent_post = Post.objects.all().order_by('-last_updated')[:3]
    featured_post = Post.objects.filter(is_featured=True).first()

    subscribe_form = SubscribeForm()
    subscribe_successful = None

    # Handle subscription form submission
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = 'Subscribed Successfully'
            request.session['subscribed'] = True
            subscribe_form = SubscribeForm()

    website_info = WebsiteMeta.objects.first() if WebsiteMeta.objects.exists() else None

    context = {
        'website_info': website_info,
        'top_post': top_post,
        'recent_post': recent_post,
        'featured_post': featured_post,
        'subscribe_form': subscribe_form,
        'subscribe_successful': subscribe_successful
    }
    return render(request, 'app/index.html', context)

# View for displaying posts by tag
def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[:3]
    featured_posts = Post.objects.filter(is_featured=True)[:3]

    context = {
        'tag': tag,
        'tags': Tag.objects.all(),
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'featured_posts': featured_posts
    }
    return render(request, 'app/tag.html', context)

# View for displaying posts by author
def author(request, slug):
    author = get_object_or_404(Profile, slug=slug)
    top_posts = Post.objects.filter(author=author.user).order_by('-view_count')[:2]
    recent_posts = Post.objects.filter(author=author.user).order_by('-last_updated')[:3]
    featured_posts = Post.objects.filter(is_featured=True)[:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')[:10]

    context = {
        'author': author,
        'top_authors': top_authors,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'featured_posts': featured_posts
    }
    return render(request, 'app/author.html', context)

# View for searching posts
def search_posts(request):
    search_query = request.GET.get('q', '')
    posts = Post.objects.filter(title__icontains=search_query)

    context = {
        'posts': posts,
        'search_query': search_query,
    }
    return render(request, 'app/search.html', context)

# View for displaying the about page
def about(request):
    website_info = WebsiteMeta.objects.first() if WebsiteMeta.objects.exists() else None

    context = {
        'website_info': website_info,
    }
    return render(request, 'app/about.html', context)

# View for displaying the contact us page
def contact_us(request):
    website_info = WebsiteMeta.objects.first() if WebsiteMeta.objects.exists() else None
    context = {
        'website_info': website_info,
    }
    return render(request, 'app/contact_us.html', context)

# View for user registration
def register(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    context = {
        'form': form,
    }
    return render(request, 'registration/registration.html', context)

# View for bookmarking a post
def bookmark_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)

    return HttpResponseRedirect(reverse('post_page', args=[slug]))

# View for displaying all bookmarked posts
def all_bookmark_post(request):
    posts = Post.objects.filter(bookmarks=request.user)

    context = {
        'posts': posts
    }
    return render(request, 'app/all_bookmark_post.html', context)

# View for displaying all liked posts
def all_liked_post(request):
    posts = Post.objects.filter(likes=request.user)

    context = {
        'posts': posts
    }
    return render(request, 'app/all_liked_post.html', context)

# View for displaying all posts
def all_post(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'app/all_post.html', context)

# View for liking a post
def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_page', args=[slug]))
