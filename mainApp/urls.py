from django.urls import path,include
from. import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product, name='product'),
    path('menu/<int:gender>', views.menu, name='menu'),
    path('about', views.about, name="about"),
    path('registration',views.registration,name="registration"),
    path("asdwa2e12daz", views.check_registration, name="reg_check"),
    path("logou", views.logou, name="logout"),
    path("delete", views.delete, name="delete"),
    path("edit", views.edit, name="edit"),
    path("reset-password", PasswordResetView.as_view(template_name="mainApp/registration/password_reset_form.html"), name="reset_password"),
    path("reset-password/done", PasswordResetDoneView.as_view(template_name="mainApp/registration/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name="mainApp/registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset-password/done", PasswordResetDoneView.as_view(template_name="mainApp/registration/password_reset_complete.html"), name="password_reset_complete")
    ]
