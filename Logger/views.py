from django.shortcuts import render
from django.http import HttpResponse


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