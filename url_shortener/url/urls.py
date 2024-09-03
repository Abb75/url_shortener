
from django.urls import path
from .views import url_view, redirect_view



urlpatterns = [
    path('url/', url_view, name='url_shortener'),
    path('<str:short_url>/', redirect_view, name='redirect_view')


]