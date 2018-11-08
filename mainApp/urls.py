

from django.urls import path,include
from. import views
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product, name='product'),
    path('menu/<int:gender>', views.menu, name='menu'),
    path('about', views.about, name="about"),
    path('registration',views.registration,name="registration"),
    path("asdwa2e12daz", views.check_registration, name="reg_check"),
    path("logou", views.logou, name="logout")
    ]
