

from django.urls import path,include
from. import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.strong, name='strong'),
    path('about1', views.strong1, name='strong1'),
    ]