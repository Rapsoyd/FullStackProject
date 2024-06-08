from django.views.generic import ListView, DetailView, UpdateView  # Импортируем базовое представление
from apps.blog.models import Post, Category
from .forms import PostUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages


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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blogs_components/post_detail.html'
    context_object_name = "post"  # Переменная с которой мы будем работать в шаблоне

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['profile'] = post.author.profile
        return context


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


@login_required
def post_create_view(request):
    categories = Category.objects.all().exclude(title='All Articles')
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('description')
        text = request.POST.get('text')
        thumbnail = request.POST.get('thumbnail')
        status = request.POST.get('status')
        Post.objects.create(title=title, category=category,
                            description=description, text=text, thumbnail=thumbnail, status=status)
    else:
        context = {
            'title': 'Создание поста',
            'categories': categories
        }
        return render(request, 'blog/blogs_components/post_create.html', context)


@login_required
def user_post_list(request):
    user = request.user
    post_list = Post.objects.all().filter(author=user)
    context = {'posts': post_list, 'title': 'Мои посты'}
    return render(request, 'blog/blogs_components/user_posts.html', context)


class PostUpdateView(UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Post
    template_name = 'blog/blogs_components/post_update.html'
    context_object_name = 'post'
    form_class = PostUpdateForm

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        if post.author != self.request.user:
            messages.error(request, 'You are not allowed to edit this post.')
            return redirect('blogs_page')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)
