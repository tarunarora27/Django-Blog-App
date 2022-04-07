from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView
)
from .forms import PostCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

'''
def home(request):
    return HttpResponse("<h1>Welcome to Blog Site</h1>")
'''

'''
def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})
'''

class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'   #by default it looks for <app>/<model>_<viewtype>  e.g posts/post_list
    context_object_name = 'posts'  #by default it looks for object but since we have posts var in template we are defining this

class PostDetailView(DetailView):
    model = Post

class MyPostListView(ListView):
    model = Post
    template_name = 'posts/myposts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user)
    '''
    def get_context_data(self, **kwargs):
        ctx = super(MyPostListView, self).get_context_data(**kwargs)
        ctx['filter'] = Post.objects.filter(author = self.request.user)
        print(ctx['filter'])
        return ctx
    '''
class UserPostListView(ListView):
    model = Post
    template_name = 'posts/userposts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        #user = self.kwargs.get('username')
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        print(type(user))   #django.contrib.auth.models.User
        return Post.objects.filter(author = user)


@login_required()
def createPost(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            #messages.success(request, "Post Created successfully!!")
            #return reverse('post-detail', kwargs={'pk': form.instance.id})
            return redirect('my-posts')
    else:
        form = PostCreationForm()
    return render(request, 'posts/create_post.html', {'form': form})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    #looks for post_confirm_delete template
    success_url = '/my_posts/'    # Necessary, to give after deleting url

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description']
    success_url = '/my_posts/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False