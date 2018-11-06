from django.shortcuts import render
import dropbox
from django.http import Http404
from .models import Product
from django.core.mail import send_mail


context = {
	"products" : Product.objects.all()
}
def index(request):
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
	return render(request, "mainApp/catalog.html", context)

def about(request):
	return render(request, "mainApp/deznaitu.html")
def registration(request):
	return render(request, "mainApp/registration.html")


def sendEmail(request):
	name = request.POST["name"]
	email = request.POST["email"]
	message = request.POST["message"]
	send_mail(
		name+' відправив вам повідомлення',
		message,
		email,
		['vadimuha13@gmail.com']
		)
	return render(request, "mainApp/Email.html")
