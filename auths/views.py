from django.shortcuts import render, redirect
from auths.forms import UserForm
from auths.models import User
from django.contrib import messages
from django.conf import settings
# Create your views here.


def register(request):
    if request.method == 'POST':
        form= UserForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
           
            user= User.objects.create_user(
                first_name=first_name, last_name=last_name,
                username=username, email=email,
                password=password,
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request,message='Success')
            return redirect('/')
            pass
        else:
            messages.error(request=request, message="Register failed!")

    else:
        form=UserForm()

    context={
        'form': form
    }
    return render(request, 'register.html',context)
    p
def activate(request,uidb64,token):
    pass
def forgotPaswword(request):
    pass
def reset_password_validate(request,uidb64,token):
    pass
def reset_password(request):
    pass
def login(request):
    pass
def logout(request):
    pass