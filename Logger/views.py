from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Users.models import bottlesDB
from .models import loggerDB
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.middleware.csrf import get_token
import datetime

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
    loggingData = loggerDB.objects.all().filter(bottleID=bottles[0].bottleID).order_by('timeStamp')
    print(bottles[0].bottleID)
    data = []
    pst_tz = datetime.timezone(datetime.timedelta(hours=-7))
    for item in loggingData:
     utc_dt = datetime.datetime.utcfromtimestamp(item.timeStamp.timestamp())

        # Create a timezone object for Pacific Standard Time (PST)

        # Convert the UTC datetime to PST
     pst_dt = utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(pst_tz)

        # Format the PST datetime as a string
     pst_str = pst_dt.strftime('%I:%M %p, %d %b, %Y')
     data.append({ 'bottleID': item.bottleID, 'measurement': item.measurement, 'timeStamp': pst_str})
    context = {
        "title" : 'Your Data',
        "loggingData" : data
    }
    # Print the PST datetime string

# Print the PST datetime string
    print(pst_str)
    return render(request, 'Logger/data.html', context)
    
