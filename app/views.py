from django.shortcuts import render
from .models import Post,Tag, Comments
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'app/index.html', context)

def tag(request, slug):
    posts = Tag.objects.get(slug = slug)
    context = {'posts':posts}
    return render(request, 'app/index.html', context)
