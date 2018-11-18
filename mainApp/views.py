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
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request
import dropbox
from django.core.mail import EmailMultiAlternatives
from twilio.rest import Client



def index(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		username = username
		username = username.lower()
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
			name+' відправив вам повідомлення '+ email,
			message,
			"aromanatali@ukr.net",
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
		username = username
		username = username.lower()
		email = email
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
		username = username
		username = username.lower()
		email = email
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
		try:
			product = Product(name="Вставте ім'я", image="0", image_name="1"+str(Product.objects.latest('id').id), description="Додайте опис", gender=-1, price=0, is_featured=0)
			product.save()
		except Product.DoesNotExist:
			product = Product(name="Вставте ім'я", image="0", image_name="1"+str("0"), description="Додайте опис", gender=-1, price=0,  is_featured=0)
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
		product.name = new_name
		product.description = new_description
		product.price = new_price
		product.gender = request.POST["gender"]
		product.is_transit = 0
		try:
			a = request.POST["featured"]
			product.is_featured = 1
		except:
			product.is_featured = 0
		product.save()
		Product.objects.filter(is_transit=1).all().delete()

		return HttpResponseRedirect(reverse("product", args= (product.id, )))
	else:
		return render("hacker.html")
def unfeature(request):
	if request.method == "POST":
		p = Product.objects.get(pk=request.POST["product_id"])
		p.is_featured = 0
		p.save()
		return JsonResponse({"status": "ok"})

def add_to_basket(request):
	if request.method == "POST":
		# request.session["basket"] = []
		# request.session["amount"] = []
		id = request.POST["id"]
		product = Product.objects.get(pk=id)
		l = [product.id]
		try:
			request.session["basket"]
		except:
			request.session["basket"] = []
		try:
			request.session["amount"]
		except:
			request.session["amount"] = []

		if l[0] not in request.session["basket"]:
			request.session["basket"] += l
			request.session["amount"] += [[1, l[0]]]
		else:
			iterator = 0
			for i in request.session["amount"]:
				if i[1] == l[0]:
					request.session["amount"][iterator][0] += 1
					request.session.modified = True
					break
				iterator+=1

		return JsonResponse({"amount": len(request.session["basket"])})

def get_products(request):
	if request.method == "POST":
		try:
			request.session["basket"]
		except:
			return JsonResponse({})
		objects = {}
		i = 0
		for product_id in request.session["basket"]:
			product = Product.objects.get(pk=product_id)
			objects[i] = {}
			objects[i]["id"] = product.id;
			objects[i]["image"] = product.image
			objects[i]["name"] = product.name
			objects[i]["price"] = product.price
			print(objects[i]["price"])
			for j in request.session["amount"]:
				if j[1] == product_id:
					objects[i]["amount_in_basket"] = j[0]
					break
			print("" + str(objects[i]["name"]) + " " + str(objects[i]["amount_in_basket"]))
			i+=1
		return JsonResponse(objects)

def change_amount(request):
	if request.method == "POST":
		new_amount = request.POST["amount"]
		prod_id = request.POST["proudct_id"]
		iterator = 0
		for i in request.session["amount"]:
			print(i)
			print(prod_id)
			if str(i[1]) == str(prod_id):
				request.session["amount"][iterator][0] = new_amount
				request.session.modified = True
				break
			iterator+=1
		return JsonResponse({"new_amount": new_amount})
def checkout(request):
	if request.method == "GET":
		if request.user.is_authenticated:
			user = Profile.objects.get(user=request.user)
			context = {
				"user": user,
				"auth": True
			}
			return render(request,"mainApp/checkout.html", context)
		else:
			context = {
				"auth": False
			}
			return render(request,"mainApp/checkout.html", context)
def send_products(request):
	if request.method == "GET":
		email = request.GET["email"]
		first_name = request.GET["first_name"]
		last_name = request.GET["last_name"]
		phone = request.GET["phone"]
		account_sid = "AC65468de5dbc455f5c5226931729f522c"
		auth_token  = "b48f1a288c190fef819feb8672498b68"
		sms = "Покупка від: " + first_name + " " + last_name + " \nТелефон: " +phone + "\nПокупка:\n" 
		html_content = " <style type=text/css media=screen>.table1 a{ margin: 0 0 0 20px; font-size: 29px;}.name1{  margin: 0  0 0 150px; font-size: 20px;}.price1{ margin: -22px 0 0 410px; font-size: 20px;}.kilkist1{  margin: -22px 0 0 565px; font-size: 20px;}.suma1{ margin: -22px 0 0 735px; font-size: 20px;}.bay1{ margin: -22px 0 0 20px; font-size: 20px;}.line1{margin: 62px 22px 22px -900px;}.foto1{margin: 9px 0 0 0;}.name_buy1{ margin: -79px 0 0 195px;font-size: 18px;}.price_buy1{ margin: -22px 0 0 225px;font-size: 18px;}.num1{margin: 0 0 0 150px;font-size: 18px;}.suma_buy1{ margin: -22px 0 0 320px; font-size: 18px;}.X1{ margin: -49px 0 0 160px;}.dw-basket1:hover{transition: all 0.5s;background: #fff;color: #2c536c;}.dw-basket1{margin: -22px 0 25px 150px;font-size: 18px;}.itog1{margin: -52px 0 22px 542px;font-size: 22px;}.all1{margin: -23px 0 22px 222px;font-size: 22px;}</style> <div id=product-wrapper> <div class=product>"
		for i in request.session["amount"]:
			p = Product.objects.get(pk=i[1])
			sms += str(p.name) +" "+str(i[0])+" шт - загальна вартість: " + str(int(p.price)*int(i[0])) + "\n"
			html_content+="<a><img src='"+ str(p.image) +"' width=160px alt=parfum class=foto1> </a> <div class=name_buy1>"+ str(p.name) +"<div class=price_buy1>"+str(p.price)+" грн <div class=num1> "+str(i[0])+" шт </div> <div class=suma_buy1>"+str(int(p.price)*int(i[0]))+" грн <div class=X1> <hr size=2 color=#C0C0C0 class=line1><br></hr> </div></div></div></div> </div>"
		html_content+="</div id='contact_info'><p>Email: "+str(email)+"</p><p>Ім'я: "+str(first_name)+"</p><p>Фамілія: "+str(last_name)+"</p><p>Телефон: "+str(phone)+"</p></div>"
		subject = "Покупка від "+ str(first_name) + " "+ str(last_name)
		from_email = "aromanatali@ukr.net"
		to = "vadimuha13@gmail.com"
		text_content = "У вас покупка"
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		client = Client(account_sid, auth_token)
		message = client.messages.create(
                	to='+380506901137',
                	from_='+14789991065',
                    body=sms       
                 )
		print(message.sid)

		featured = Product.objects.filter(is_featured=1)
		context = {
			"products" : featured,
			"message" : "Ваш заказ прийнятий, з вами зв'яжуться найближчим часом",
			"auth": request.user.is_authenticated,
			"admin": request.user.is_staff,
		}
		request.session["basket"] = []
		request.session["amount"] = []
		return render(request,'mainApp/homePage.html', context)
def delete_from_cart(request):
	if request.method == "POST":
		p_id = request.POST["id"]
		iterator = 0
		print(request.session["basket"])
		print(type(request.session["basket"][0]))
		print(p_id)
		print(type(p_id))
		request.session["basket"].remove(int(p_id))
		print(request.session["basket"])
		for i in request.session["amount"]:
			if i[1] == int(p_id):
				print(request.session["amount"][iterator])
				del request.session["amount"][iterator]
				print(request.session["amount"][iterator])
				break
			iterator += 1
		print(request.session["basket"])
		print(request.session["amount"])
		request.session.modified = True
		return JsonResponse({"status": "ok"})