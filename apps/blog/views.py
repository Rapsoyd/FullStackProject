from django.views.generic import ListView, DetailView, CreateView, UpdateView, View  # Импортируем базовое представление
from apps.blog.models import Post, Category, Comment
from .forms import PostCreateForm, PostUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect('blogs_page')
    return render(request, 'index.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/blogs.html'
    context_object_name = "posts"
    paginate_by = 2
    queryset = Post.custom.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)  # Получаем базовые контекстные данные
    #     context['title'] = 'Главная страница'
    #     return context


class PostDetailView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = post.comments.all()
        return render(request, 'blog/blogs_components/post_detail.html', {'post': post, 'comments': comments})


class PostFromCategory(ListView):
    template_name = "blog/blogs.html"
    context_object_name = "posts"
    category = None
    paginate_by = 2

    def get_queryset(self):
        # Закладываем данные в атрибут ЭК и извлекаем в равенстве фильтра параметр slug из URL запроса
        self.category = Category.objects.get(slug=self.kwargs["slug"])
        # Получаем список постов с переданным в URL slug
        queryset = Post.custom.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.objects.filter(category__in=sub_cat)
        return queryset


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/blogs_components/post_create.html"
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Post
    template_name = 'blog/blogs_components/post_update.html'
    context_object_name = 'post'
    form_class = PostUpdateForm

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, View):
    login_url = '/user/login/'  # URL Для перенаправления пользователя на страницу логина
    redirect_field_name = 'next'  # Параметр

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent')Сщ
        user = request.user

        if parent_id:
            parent = Comment.objects.get(id=parent_id)
        else:
            parent = None

        Comment.objects.create(
            author=user,
            post=post,
            content=content,
            parent=parent
        )

        return redirect('post_detail', slug=post.slug)
