from django.shortcuts import render
import dropbox
from django.http import Http404, HttpResponse
from .models import Product, Profile
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password


def index(request):
	if request.method == "POST":

		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if not user:
			return JsonResponse({"authentification": 0})
		else:
			return JsonResponse({"authentification": 1})
		context = {
			"products" : Product.objects.filter(is_featured=1),
			"message" : ""
		}
		return render(request,'mainApp/homePage.html', context)
	else:
		context = {
			"products" : Product.objects.filter(is_featured=1),
			"message" : ""
		}
		return render(request,'mainApp/homePage.html', context)

def product(request, product_id):
	try:
		product = Product.objects.get(pk = product_id)
	except Product.DoesNotExist:
		raise Http404("Product does not exist")
	context = {
		"product" : product
	}
	return render(request,'mainApp/ProductPage.html', context)
def menu(request):
	context = {
		"products" : Product.objects.all()
	}
	return render(request, "mainApp/catalog.html", context)

def about(request):
	if request.method == "POST":
		name = request.POST["name"]
		email = request.POST["email"]
		message = request.POST["message"]
		send_mail(
			name+' відправив вам повідомлення',
			message,
			email,
			['vadimuha13@gmail.com']
			)
		context = {
			"products" : Product.objects.filter(is_featured=1),
			"message" : "Ваше повідомлення відправлене"
		}
		return render(request, "mainApp/homePage.html", context)
	else:
		return render(request, "mainApp/deznaitu.html")

def registration(request):
	if request.method == "POST":
		fname = request.POST["fіrstname"]
		sname = request.POST["lastname"]
		email = request.POST["email"]
		phone = request.POST["phone"]
		password = request.POST["password"]
		username = request.POST["username"]
		user = User(username=username,first_name=fname, last_name=sname, email=email, password=make_password(password))
		user.save()
		
		profile = Profile(user=user, phone_number=phone)
		profile.save()
		context = {
			"products" : Product.objects.filter(is_featured=1),
			"message" : "Вас зареєстровано"
		}
		return render(request, "mainApp/homePage.html", context)
	else:
		return render(request, "mainApp/registration.html")




