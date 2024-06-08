from django.urls import path
from .views import user_post_list, PostListView, PostDetailView, PostFromCategory, post_create_view, PostUpdateView, index

urlpatterns = [
    path("", index, name='index'),
    path("blogs/", PostListView.as_view(), name="blogs_page"),
    path('post/create/', post_create_view, name='post_create'),
    path('post/user_posts', user_post_list, name='user_posts'),
    path('post/<str:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path("post/<str:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("category/<str:slug>/", PostFromCategory.as_view(), name="post_by_category")
]
