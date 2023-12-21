import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
import stripe
from django.conf import settings
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from.models import Item
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *
from payment.tasks import send_test_message
from rest_framework import generics
from .serializers import ItemSerializer


stripe.api_key = settings.SECRET_API_KEY

# получение session_id
class BuyItemView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=item_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.price * 100),
                        'product_data': {
                            'name': item.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": item.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    
# платеж проведен успешно
class SuccessView(TemplateView):
    template_name = "payment/success.html"

# отмена платежа
class CancelView(TemplateView):
    template_name = "payment/cancel.html"

# вывод отпределенного товара
class ItemView(DetailView):
    context_object_name = 'item'
    template_name = 'payment/detail_item.html'
    model = Item

# вывод списка товаров
class ItemList(ListView):
    context_object_name = 'items'
    template_name = 'payment/main.html'
    model = Item

# view авторизации
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'payment/login.html', {'form': form})

# view выхода из аккаунта
def user_logout(request):
    logout(request)
    return redirect('home')

# view регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_test_message.delay(form.cleaned_data['email'])
            messages.success(request, 'Успешная регистрация')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'payment/register.html', {'form': form})



# Serializers View

# Вывод списка товаров
class ItemAPIList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Обновление и удаление товара
class ItemAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer