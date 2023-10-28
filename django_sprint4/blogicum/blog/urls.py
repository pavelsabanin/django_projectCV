from django.urls import path, include

from . import views

app_name = 'blog'

post_urls = [
    path('/create/', views.PostCreateView.as_view(), name='create_post'),
    path('/<int:pk>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('/<post_id>/comment/edit/<int:pk>/',
         views.CommentUdpateView.as_view(), name='edit_comment'),
    path('/<post_id>/delete_comment/<int:pk>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
    path('/<int:pk>/comment/',
         views.CommentCreateView.as_view(), name='add_comment'),
    path('/<int:pk>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('/<int:pk>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),

]
urlpatterns = [
    path('posts', include(post_urls)),
    path('', views.PostListView.as_view(), name='index'),
    path('profile/<str:username>/',
         views.ProfileListView.as_view(), name='profile'),
    path('profile/edit/<slug:username>/',
         views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts')
]
