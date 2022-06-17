from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Comments
from .forms import PostForm
from django.shortcuts import render, get_object_or_404

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    comments = Comments.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list.html', {'posts': posts}) #, {'comments': comments})

def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_edit(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})