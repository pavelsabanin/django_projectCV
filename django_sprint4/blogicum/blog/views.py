from datetime import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import ListView, CreateView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin

from .forms import CommentForm, PostForm, UserForm
from blog.models import Post, Category, Comment

NUMBER_OF_POSTS = 10


class PostListView(ListView):
    model = Post
    paginate_by = NUMBER_OF_POSTS
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comment_count=Count('comments')).filter(
            is_published=True, category__is_published=True,
            pub_date__lte=datetime.now()).order_by('-pub_date')
        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={
            'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class CategoryListView(ListView):
    model = Post
    paginate_by = NUMBER_OF_POSTS
    fields = '__all__'
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'],
            is_published=True, created_at__lte=datetime.now())
        return Post.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True, pub_date__lte=datetime.now(),).annotate(
            comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_published:
            if request.user != instance.author:
                raise Http404('Нет доступа')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')

        return context


class CommentUdpateView(UpdateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise Http404("У вас нет прав на изменение этого комментария.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['post_id']})


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS

    def get_queryset(self):
        username = self.kwargs['username']
        self.profile = get_object_or_404(User, username=username)
        return Post.objects.filter(author=self.profile).annotate(
            comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user_form.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs['username']
        if self.request.user.username != username:
            return redirect('blog:profile', username=username)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    posts = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.posts
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.posts.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise Http404("У вас нет прав на изменение этого комментария.")
        self.posts = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.posts.pk})
