from django.urls import path

from .views import add_comment_view


app_name = "comments"

urlpatterns = [
    path('add_comment/<int:book_id>', add_comment_view, name='add_comment'),
]
