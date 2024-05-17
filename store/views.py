from django.shortcuts import render

# Create your views here.
def index(request):
    return render (request, 'index.html')

def product_details(request,slug):
    pass
def wishlist(request):
    return render (request, 'wishlist.html')
    pass
def add_wishlist(request):
    pass
def sreach(request):
    pass
def submit_review(request):
    pass
def add_to_cart(request):
    pass
def update_cart(request):
    pass
def delete_cart(request):
    pass
def cart_details(request):
    pass
def checkout(request):
    pass
def contact(request):
    return render (request, 'contact.html')
def about(request):
    return render (request, 'about.html')