from django.shortcuts import render, redirect
from django.urls import reverse
from auths.forms import UserForm
from typing import Protocol
from auths.models import User
from django.contrib import messages
from .decorator import user_not_authenticated
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.conf import settings
from django.views import View
from django.contrib import auth

@user_not_authenticated
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
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if len(password) < 6:
                        messages.error(request, 'Password too short')
                        return redirect('register')
                    
                    user= User.objects.create_user(
                        first_name=first_name, last_name=last_name,
                        username=username, email=email,
                        password=password,
                    )
                    user.phone_number = phone_number
                    user.is_active = False
                    user.save()
                    mail_subject = "Activate your user account."
                    current_site = get_current_site(request)
                    email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    }
                   
                    link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})
                    
                    activate_url = 'http://'+current_site.domain+link
                    email = EmailMessage(
                    mail_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                    email.send(fail_silently=False)
                    messages.success(request,message='Successfully registered')
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


def activate( request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        email = request.POST['useremailname']
        password = request.POST['password']

        if email and password:
            user = auth.authenticate(email=email, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'login.html')


def forgotPaswword(request):
    pass
def reset_password_validate(request,uidb64,token):
    pass
def reset_password(request):
    pass

    pass
def logout(request):
    pass