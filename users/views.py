from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction

from books_app.models import Book
from .forms import CustomUserCreationForm, CustomAuthenticationForm


@login_required(login_url='users:login')
def view_profile(request):
    user_books = Book.objects.filter(seller=request.user)
    return render(request, 'users/profile.html', {'user_books': user_books})


@transaction.atomic
def register_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
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


def logout_view(request):
    logout(request)

    return redirect('books:index')
