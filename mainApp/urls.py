

from django.urls import path,include
from. import views
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product, name='product'),
    path('about1', views.strong1, name='strong1'),
    ]