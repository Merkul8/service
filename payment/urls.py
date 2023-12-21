from django.urls import path
from .views import *
from django.conf import settings


urlpatterns = [
    path('', ItemList.as_view(), name='home'),
    path('item/<int:pk>', ItemView.as_view(extra_context = {"STRIPE_PUBLIC_KEY": settings.PUBLIC_API_KEY}), name='item'),
    path('buy/<int:pk>', BuyItemView.as_view(), name='buy'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    # Регистрация и авторизация
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # drf views
    path('items/', ItemAPIList.as_view(), name='items_drf'),
    path('items/<int:pk>/', ItemAPIDetail.as_view(), name='item_drf')
]