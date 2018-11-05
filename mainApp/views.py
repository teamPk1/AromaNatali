from django.shortcuts import render
import dropbox
from django.http import Http404
from .models import Product



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

