from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from books_app.models import Book
from comments_app.models import Comment
from order_app.models import Order
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    UserProfileEditForm,
    CustomPasswordChangeForm
)
from .utils import is_admin


@login_required(login_url='users:login')
def view_profile(request: HttpRequest) -> HttpResponse:
    user = request.user

    if user.status == 'customer':
        customer_orders = Order.objects.filter(user=user)
        user_books = None
    else:
        customer_orders = None
        user_books = Book.objects.filter(seller=user)

    context = {
        'user_books': user_books,
        'customer_orders': customer_orders
    }

    return render(request, 'users/profile.html', context)


@login_required(login_url='users:login')
@user_passes_test(is_admin)
def view_admin_dashboard(request: HttpRequest) -> HttpResponse:
    books = Book.objects.filter(is_verified=False)
    comments = Comment.objects.filter(is_verified=False)
    orders = Order.objects.filter(payment_status='unpaid')

    context = {
        'books': books,
        'comments': comments,
        'orders': orders
    }

    return render(request, 'users/admin.html', context)


@transaction.atomic
def register_user_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('books:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)

    return redirect('books:index')


@login_required(login_url='users:login')
def edit_profile_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileEditForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:profile')
