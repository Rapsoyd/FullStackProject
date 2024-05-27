from django.urls import path
from .views import PostListView, PostDetailView, PostFromCategory, PostCreateView, PostUpdateView, index

urlpatterns = [
    path("", index, name='index'),
    path("blogs/", PostListView.as_view(), name="blogs_page"),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<str:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path("post/<str:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("category/<str:slug>/", PostFromCategory.as_view(), name="post_by_category")
]
