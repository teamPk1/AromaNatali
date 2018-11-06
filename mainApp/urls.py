

from django.urls import path,include
from. import views
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product, name='product'),
    path('menu', views.menu, name='menu'),
    path('about', views.about, name="about"),
<<<<<<< HEAD
    path('registration',views.registration,name="registration")
=======
    path("128asd122819u", views.sendEmail, name="sendEmail")
>>>>>>> e248d1485cee3c2e4eec00de79301fb2751c871e
    ]