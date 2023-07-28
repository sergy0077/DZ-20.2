# from django.urls import path
# from catalog.views import home
# from catalog.views import contacts
#
#
# urlpatterns = [
#     path('', home)
#
# ]
#
# urlpatterns = [
#     path('', contacts)
#
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]
