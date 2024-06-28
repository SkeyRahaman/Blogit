from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('post/<slug:slug>', views.post_page, name = 'post_page'), 
    path('tag/<slug:slug>', views.tag, name='tag_page'),
    path('author/<slug:slug>', views.author, name='author_page'),
    path('search/', views.search_posts, name='search_page'),
    path('all_post/', views.all_post, name='all_post_page'),
    path('about/', views.about, name='about_page'),
    path('contact/', views.contact_us, name='contact_page'),
    path('accounts/register/', views.register, name='register')
]
