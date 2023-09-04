from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from blog.models import Blog
from django.shortcuts import render


def is_moderator(user):
    return user.groups.filter(name='Модераторы').exists()
def is_owner(user):
    return user.groups.filter(name='Владельцы').exists()


"""Контроллеры"""

class BlogCreateView(CreateView):
    """создания блога для новой статьи"""

    model = Blog
    fields = ('title', 'description', 'creation_date', 'preview', 'is_published')
    success_url = reverse_lazy('blog:list')
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        """slug-name для заголовка"""
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
            return HttpResponseRedirect(
                self.success_url)  # Указываем явно, куда перенаправлять после успешного создания
        else:
            print(form.errors)
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})  # Отобразить форму с ошибками


class BlogListView(ListView):
    """блога для просмотра статей"""

    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        """выводим в общий список опубликованные записи"""

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset


class BlogDetailView(DetailView):
    """блога для детального просмотра статьи"""

    model = Blog

    def get_object(self, queryset=None):
        """Счетчик просмотров"""

        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ('title', 'description', 'creation_date', 'preview', 'is_published')

    def test_func(self):
        """Проверка, имеет ли пользователь право редактировать статьи"""
        user = self.request.user
        return user.is_staff or is_moderator(user)

    def get_success_url(self):
        """Переопределение url-адреса для перенаправления после успешного редактирования"""
        return reverse('blog:view', args=[self.object.pk])


class BlogDeleteView(DeleteView):
    """блога для удаления статьи"""
    model = Blog
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        """Проверка, имеет ли пользователь право удалять статью."""
        user = self.request.user
        return user.is_staff  # Только модераторы могут удалять статьи

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("У вас нет прав для удаления этой статьи.")
        return super().dispatch(request, *args, **kwargs)
