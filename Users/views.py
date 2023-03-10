from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import bottlesDB
from .models import authDB
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
import random
import string

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")

            # Adding data to logerrer table in database
            log = bottlesDB()
            log.username = form.cleaned_data.get("username")
            log.bottleID = form.cleaned_data.get("bottleID")
            log.save()

            email = form.cleaned_data.get("email")

            auth = authDB()
            auth.username = form.cleaned_data.get("username")
            auth.isVerified = False

            letters = string.ascii_lowercase
            optToVerify = ''.join(random.choice(letters) for _ in range(8))
            auth.otpToVerify = optToVerify

            auth.save()
            send_email(email, form.cleaned_data.get("username"),
                       form.cleaned_data.get("first_name"), optToVerify)
            messages.success(
                request, f'Your account has been created, you can proceed to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            data = authDB.objects.get(username=username)
            if data.isVerified:
                auth_login(request, user)  
                return render(request, 'Logger/home.html', {'username': username})
                # return render(request, 'Logger/home.html')
            else:
                messages.error(
                    request, f'Please verify account via email before logging in')
        else:
            messages.error(request, f'Invalid credentials, try again')

    else:
        form = AuthenticationForm()
    return render(request, 'Users/login.html', {'form': form})


def send_email(email, username, first_name, optToVerify):
    subject = 'Welcome to WaterWise '+first_name+'!'
    message = 'Thank you for signing up to Waterwise, Your username is '+username + \
        '\n Please click this link to verify your email.\n http://localhost:8000/verifyuser?username='+username+'&opt='+optToVerify
    from_email = 'waterwise-noreply@razlator.online'
    recipient_list = [email]
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


def verifyuser(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        optToVerify = request.GET.get('opt')
        auth = authDB.objects.get(username=username)
        if optToVerify == auth.otpToVerify:
           auth.isVerified = True
           auth.save()
           messages.success(request, f'Verificaation successful, try loggining in now')
        else:
            messages.error(request, f'something went wrong please contact support')
    return render(request, 'Users/verification.html')
