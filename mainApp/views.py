from django.shortcuts import render
import dropbox
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Product, Profile
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request
import dropbox



def index(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if not user:
			return JsonResponse({"authentification": 0})
		else:
			login(request, user)
			return JsonResponse({"authentification": 1})
	else:
		featured = Product.objects.filter(is_featured=1)
		context = {
			"products" : featured,
			"message" : "",
			"auth": request.user.is_authenticated,
			"admin": request.user.is_staff,
		}
		return render(request,'mainApp/homePage.html', context)

def product(request, product_id):
	try:
		product = Product.objects.get(pk = product_id)
	except Product.DoesNotExist:
		raise Http404("Product does not exist")
	context = {
		"product" : product,
		"auth": request.user.is_authenticated,
		"admin": request.user.is_staff
	}
	return render(request,'mainApp/ProductPage.html', context)
def menu(request, gender):
	context = {
		"products" : Product.objects.filter(is_transit = 0),
		"auth": request.user.is_authenticated,
		"admin": request.user.is_staff,
		"gender": gender
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
			"message" : "Ваше повідомлення відправлене",
			"auth": request.user.is_authenticated,
			"admin": request.user.is_staff
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
		password2 = request.POST["password1"]
		username = request.POST["username"]
		username = username.upper()
		email = email.upper()
		if username =="" or password == "" or phone == "" or email == "" or sname == "" or fname == "":
			context = {
				"products" : Product.objects.filter(is_featured=1),
				"message" : "Потрібно заповнити всі поля",
				"auth": request.user.is_authenticated,
				"admin": request.user.is_staff
			}
			return render(request, "mainApp/homePage.html", context)		
		if password != password2:
			context = {
				"products" : Product.objects.filter(is_featured=1),
				"message" : "Паролі не співпадають",
				"auth": request.user.is_authenticated,
				"admin": request.user.is_staff
			}
			return render(request, "mainApp/homePage.html", context)	
		if authenticate(request, username=username, password=password) == None:
			if User.objects.filter(email=email):
				context = {
					"products" : Product.objects.filter(is_featured=1),
					"message" : "Такий email уже зареєстровано",
					"auth": request.user.is_authenticated,
					"admin": request.user.is_staff
				}
				return render(request, "mainApp/homePage.html", context)
			user = User(username=username,first_name=fname, last_name=sname, email=email, password=make_password(password))
			user.save()
			profile = Profile(user=user, phone_number=phone)
			profile.save()
			login(request, user)
			context = {
				"products" : Product.objects.filter(is_featured=1),
				"message" : "Вас зареєстровано",
				"auth": request.user.is_authenticated,
				"admin": request.user.is_staff
			}
			return render(request, "mainApp/homePage.html", context)
		else:
			context = {
				"products" : Product.objects.filter(is_featured=1),
				"message" : "Такий користувач уже зареєстрований",
				"auth": request.user.is_authenticated,
				"admin": request.user.is_staff
			}
			return render(request, "mainApp/homePage.html", context)	
	else:
		return render(request, "mainApp/registration.html")



def check_registration(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		username = username.upper()
		email = email.upper()
		if User.objects.filter(email=email):
			return JsonResponse({
					'existance': 1
				})
		elif User.objects.filter(username=username):
			return JsonResponse({
				'existance': 2
				})
		else:
			return JsonResponse({
				'existance': 0
				})
	else:
		return render(request, "mainApp/hacker.html")

def logou(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))
def delete(request):
	if request.method == "POST":
		product_id = request.POST["id"]
		product = Product.objects.get(pk=product_id)
		product.delete()
		return JsonResponse({'status': 1})
	else:
		return render("mainApp/hacker.html")
def add(request):
	if request.method == "GET":
		product = Product(name="Вставте ім'я", image="0", image_name="1"+str(Product.objects.latest('id').id), description="Додайте опис", gender=-1, price=0, amount_present=0, is_featured=0)
		product.save()
		context = {
			"product" : product,
			"auth": request.user.is_authenticated,
			"admin": request.user.is_staff
		}
		return render(request,'mainApp/ProductPage.html', context)
		
def edit(request):
	if request.method == "POST":
		product = Product.objects.get(pk=request.POST["id"])
		try:		
			myfile = request.FILES["image"]
			dbx = dropbox.Dropbox('JMO11L9PvLAAAAAAAAAACeGJKD2QE2UDr-_VpCi0U_RDdMPlp40EJyBBM9-pSjdc')			
			
			new_product_name = "/a" + product.image_name
			dbx.files_upload(File(myfile.open()).read(), new_product_name, mute=True)
			
			l = dbx.sharing_create_shared_link_with_settings(new_product_name).url
			n = ""
			i = 0
			while i < len(l):
				if(l[i] == "?"):
					break
				n = n + "" + l[i]
				i+=1
			n = n+"?raw=1"
			product.image = n
			product.image_name = new_product_name
			product.save()
		except:
			pass
		new_name = request.POST["name"]
		new_description = request.POST["description"]
		new_price = request.POST["price"]
		new_stock = request.POST["stock"]
		product.name = new_name
		product.description = new_description
		product.price = new_price
		product.amount_present = new_stock
		product.gender = request.POST["gender"]
		product.is_transit = 0
		if request.POST["featured"] == "on":
			product.is_featured = 1
		else:
			product.is_featured = 0
		product.save()
		Product.objects.filter(is_transit=1).all().delete()

		return HttpResponseRedirect(reverse("product", args= (product.id, )))
		# else:
		# 	return JsonResponse({"status": 0})
	else:
		return render("hacker.html")
def unfeature(request):
	if request.method == "POST":
		p = Product.objects.get(pk=request.POST["product_id"])
		p.is_featured = 0
		p.save()
		return JsonResponse({"status": "ok"})