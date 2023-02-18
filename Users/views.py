from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import loggerDB
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            
            #Adding data to logerrer table in database
            log = loggerDB()
            log.username = form.cleaned_data.get("username")
            log.bottleID = form.cleaned_data.get("bottleID")
            log.save()

            messages.success(request, f'Your account has been created, you can proceed to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})