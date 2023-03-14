from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Users.models import bottlesDB
from .models import loggerDB
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.middleware.csrf import get_token
import datetime
import decimal

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
        # Check if Bottle has been registered to username
        if bottlesDB.objects.all().filter(bottleID=bottleIDQ).exists() == True:
            # Add logging information to loggerDB table
            newMeasurement = loggerDB(
                bottleID=bottleIDQ, measurement=measurementQ)
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
    loggingData = loggerDB.objects.all().filter(
        bottleID=bottles[0].bottleID).order_by('-timeStamp')
    data = []
    waterConsumed = decimal.Decimal()
    pst_tz = datetime.timezone(datetime.timedelta(hours=-7))
    for item in loggingData:

        utc_dt = datetime.datetime.utcfromtimestamp(item.timeStamp.timestamp())
        utcCurrent_dt = datetime.datetime.utcfromtimestamp(
            datetime.datetime.now().timestamp())

        # Convert the UTC datetime to PST
        pst_dt = utc_dt.replace(
            tzinfo=datetime.timezone.utc).astimezone(pst_tz)

        pstCurrent_dt = utcCurrent_dt.replace(
            tzinfo=datetime.timezone.utc).astimezone(pst_tz)

        dayTimeStampoffset = pstCurrent_dt.hour * 3600 + pstCurrent_dt.minute * 60
        print("here")
        startTimeInFloat = float(
            int(pstCurrent_dt.timestamp())-dayTimeStampoffset)
        startTimeInDateUTC = datetime.datetime.utcfromtimestamp(
            startTimeInFloat)
        startTimeInDatePST = startTimeInDateUTC.replace(
            tzinfo=datetime.timezone.utc).astimezone(pst_tz)
        # dayStartTimeStamp = pst_dt.timestamp() -
        print(startTimeInDatePST.timestamp())
        if pst_dt.timestamp() <= pstCurrent_dt.timestamp() and pst_dt.timestamp() >= startTimeInDatePST.timestamp():
            waterConsumed = waterConsumed + item.measurement
            # Format the PST datetime as a string
        pst_str = pst_dt.strftime('%I:%M %p, %d %b, %Y')
        data.append({'bottleID': item.bottleID,
                    'measurement': item.measurement, 'timeStamp': pst_str})
        print(waterConsumed)
    context = {
        "title": 'Your Data',
        "loggingData": data,
        "waterConsumed": waterConsumed
    }
    # Print the PST datetime string

# Print the PST datetime string
    return render(request, 'Logger/data.html', context)
