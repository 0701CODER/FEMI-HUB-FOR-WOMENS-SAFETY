from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
path('',views.home,name="home"),
path('dashboard/',views.dashboard,name="dashboard"),
path('register/',views.register,name="register"),
path('login/', views.user_login, name='user_login'),
path('logout/', views.logout, name='logout'),
path('add_post/', views.add_post, name='add_post'),
path('post/', views.post, name='post'),
path('delete/<int:pk>/', views.delete, name='delete'),
path('all_post/', views.all_post, name='all_post'),
path('post_comment/<int:pk>/', views.post_comment, name='post_comment'),
path('like_post/<int:pk>/', views.like_post, name='like_post'),
path('report_post/<int:pk>/', views.report_post, name='report_post'),
path('women_rights/', views.women_rights, name='women_rights'),
path('ngo/', views.ngo, name='ngo'),
path('all_users/', views.all_users, name='all_users'),
path('follow/<int:pk>/', views.follow, name='follow'),
path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
path('profile/<int:pk>/', views.profile, name='profile'),
path('friends_list/', views.friends_list, name='friends_list'),
path('edit_profile/', views.edit_profile, name='edit_profile'),
]