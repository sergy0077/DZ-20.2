from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from blog.models import Blog
from .forms import ProductForm, ProductVersionForm
from .models import Product, Version, Category
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView


class IndexView(View):
    """Контроллер для отображения страницы со списком всех продуктов"""
    model = Product
    template_name = 'catalog/index.html'

    def get(self, request):
        products = Product.objects.all()

        for product in products:
            active_version = product.version_set.filter(is_active=True).first()
            if active_version:
                product.active_version_number = active_version.version_number
                product.active_version_name = active_version.version_name
            else:
                product.active_version_number = None
                product.active_version_name = None

        return render(request, self.template_name, {'products': products})


class ProductDetailView(View):
    """Контроллер для отображения продуктов."""
    model = Product
    template_name = 'catalog/product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, self.template_name, {'product': product})

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        context_data['title'] = f'Товар из категории: {product.category}'

        active_version = Version.objects.filter(product=self.object, is_active=True).last()
        if active_version:
            context_data['active_version_number'] = active_version.number
            context_data['active_version_name'] = active_version.name
        else:
            context_data['active_version_number'] = None
            context_data['active_version_name'] = None

        return context_data


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории товаров'
    }


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ProductCreateView(CreateView):
    """Контроллер для создания новых продуктов пользователем."""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/product_form.html'
    extra_context = {
        'title': 'Добавить новый продукт:'
    }

    def form_valid(self, form):
        """Валидатор запрещенных слов"""
        form.instance.clean()  # Вызов валидации перед сохранением
        # Сначала вызываем метод form_valid класса-родителя, чтобы создать объект Product
        response = super().form_valid(form)

        # Создание новой версии
        version_number = form.cleaned_data['version_number']
        version_name = form.cleaned_data['version_name']
        is_active = form.cleaned_data['is_active']

        version = Version(
            product=form.instance,
            version_number=version_number,
            version_name=version_name,
            is_active=is_active
        )
        version.save()

        form.instance.active_version = version_name  # Установка активной версии
        self.object.active_versions.set(form.cleaned_data['active_versions'])
        return response


class ProductUpdateView(UpdateView):
    """Контроллер для редактирования продуктов"""
    model = Product
    form_class = ProductVersionForm
    template_name = 'catalog/product_edit_form.html'
    success_url = reverse_lazy('catalog:index')
    extra_context = {
        'title': 'Редактировать продукт:'
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.active_versions.set(form.cleaned_data['active_versions'])
        return response


class ProductDeleteView(DeleteView):
    """Контроллер для удаления продуктов"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:index')
    extra_context = {
        'title': 'Удаление записи:'
    }


#########################################################################

def contacts(request):
    """Контроллер для отображения контактной информации."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts.html')


#########################################################################

def blog_list_view(request):
    """Контроллер для отображения блоговой информации."""
    blogs = Blog.objects.all()
    return render(request, 'blog/list.html', {'blogs': blogs})