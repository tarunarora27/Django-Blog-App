from django.urls import path, include
from . import views
from .views import (
    PostListView,
    PostDetailView,
    MyPostListView,
    PostDeleteView,
    PostUpdateView,
    UserPostListView
)
urlpatterns = [

    #Func based home view
    #path('', views.home, name='home'),

    # Class based home view
    path('', PostListView.as_view(), name='home'),  #ListView
    path('user_posts/<slug:username>/', UserPostListView.as_view(), name = 'user-posts'),  #ListView
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'), #DetailView
    path('my_posts/', MyPostListView.as_view(), name = 'my-posts'), #ListView
    path('my_posts/delete/<int:pk>/', PostDeleteView.as_view(), name = 'post-delete'), #DeleteView
    path('my_posts/update/<int:pk>/', PostUpdateView.as_view(), name = 'post-update'), #UpdateView
    path('post/create/', views.createPost, name = 'create')
]