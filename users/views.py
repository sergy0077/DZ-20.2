from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from utils.utils import confirm_user_email, create_secret_key


class RegisterView(CreateView):
    """Контроллер регистрации нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    """Контроллер создания профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile_view')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    """Конроллер для операций внутри аккаунта пользователя"""
    model = User

    def get_object(self, queryset=None):
        return self.request.user


"""МЕТОДЫ"""


def confirm_email(request):
    """для подтверждения почты"""
    confirm_user_email(request, request.user)
    return redirect(reverse('users:profile'))


def activate_email(request, key):
    """для активации почты"""
    print(request.user.email_confirm_key, key, sep='\n')
    if request.user.email_confirm_key == key:
        request.user.email_is_confirmed = True
        request.user.email_confirm_key = None
        request.user.save()
    else:
        print('Ключ не актуален')
    return redirect('/')


def password_reset(request):
    """для генерации пароля для неавторизованного пользователя"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = create_secret_key(12)
            user.set_password(new_password)
            user.save()
            login(request, user)

            send_mail(
                subject='Вы сменили пароль',
                message=f'Новый пароль {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email]
            )
            return redirect(reverse("users:login"))
        except User.DoesNotExist:
            return render(request, 'users/password_reset_form.html',
                          {'error_message': 'Такой пользователь не существует'})
    return render(request, 'users/password_reset_form.html')


