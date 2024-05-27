from django.views.generic import ListView, DetailView, CreateView, UpdateView  # Импортируем базовое представление
from apps.blog.models import Post, Category
from .forms import PostCreateForm, PostUpdateForm
from django.shortcuts import render


def index(request):
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
    template_name = 'blog/post_detail.html'
    context_object_name = "post"  # Переменная с которой мы будем работать в шаблоне


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
    template_name = "blog/post_create.html"
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
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    form_class = PostUpdateForm


    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)
