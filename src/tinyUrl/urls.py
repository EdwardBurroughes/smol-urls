from django.urls import path
from urlShortener import views

urlpatterns = [
    path("", views.ShortenURL.as_view(), name="shorten-url"),
    path("<str:shortened_id>/delete", views.ShortenURL.as_view(), name="delete-shortened-url"),
    path("<str:shortened_id>", views.ShortenURL.as_view(), name="redirect-url"),
]
