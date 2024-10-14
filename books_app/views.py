from django.shortcuts import render

def view_books(request):
    return render(request, "books/index.html")
