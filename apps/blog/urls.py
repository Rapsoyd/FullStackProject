from django.urls import path
from .views import (PostListView, PostDetailView, PostFromCategory,
                    PostCreateView, PostUpdateView, index, CommentCreateView)

urlpatterns = [
    path("", index, name='index'),
    path("blogs/", PostListView.as_view(), name="blogs_page"),
    path('post/comment/create/<int:post_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<str:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path("post/<str:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("category/<str:slug>/", PostFromCategory.as_view(), name="post_by_category")
]
