from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Users.models import bottlesDB
from .models import loggerDB
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.middleware.csrf import get_token

# Create your views here.
def home(request):
    # context = {
    #     'title': "Home",            
    #     # 'query_results' : referrer.objects.all().filter(company=query).order_by('firstName') | referrer.objects.all().filter(firstName=query).order_by('lastName') | referrer.objects.all().filter(lastName=query).order_by('firstName')
    # }   
    # return render(request, 'Logger/home.html', context)
    return render(request, 'Logger/home.html', {'title': 'Home'})
    # return HttpResponse("Hello, world. You're at the polls index.")



def about(request):
    return render(request, 'Logger/about.html', {'title': 'About'})


@csrf_exempt
def logging(request):
    if request.method == "POST":
        usernameQ = request.POST.get('username', None)
        bottleIDQ = request.POST.get('bottleID', None)
        # timeStampQ = request.POST.get('timeStamp', None)
        measurementQ = request.POST.get('measurement', None)

        #Check if Bottle has been registered to username
        if bottlesDB.objects.all().filter(username=usernameQ, bottleID=bottleIDQ).exists() == True:
            #Add logging information to loggerDB table
            newMeasurement = loggerDB(username=usernameQ, bottleID=bottleIDQ, measurement=measurementQ)
            newMeasurement.save() 
            messages.success(request, f'Logged')
            return render(request, 'Logger/logging.html', {'title': 'Success'})
    else:
        return render(request, 'Logger/logging.html', {'title': 'Failed'})
    