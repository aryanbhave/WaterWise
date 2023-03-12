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
    if request.method == "GET":
        bottleIDQ = request.GET.get('bottleID', None)
        measurementQ = request.GET.get('measurement', None)
        #Check if Bottle has been registered to username
        if bottlesDB.objects.all().filter(bottleID=bottleIDQ).exists() == True:
            #Add logging information to loggerDB table
            newMeasurement = loggerDB(bottleID=bottleIDQ, measurement=measurementQ)
            newMeasurement.save() 
            messages.success(request, f'Logged')
            return HttpResponse("Logged")
    else:
        return HttpResponse("FailedToLog")
    

@login_required
def data(request):
    # if request.user.is_authenticated():
    username = request.user.username
    bottles = bottlesDB.objects.all().filter(username=username)
    print(bottles[0].bottleID)
    context = {
        "title" : 'Your Data',
        "loggingData" : loggerDB.objects.all().filter(bottleID=bottles[0].bottleID).order_by('timeStamp')
    }
    return render(request, 'Logger/data.html', context)
    
