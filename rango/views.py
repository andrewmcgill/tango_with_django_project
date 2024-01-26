from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

def index(request):
    # query db for a list of cats
    # order cats by likes in desc order
    # retrieve top 5
    # put into context dict
    # pass to temp engine
    
    category_list = Category.objects.order_by('-likes')[:5]
    
    # boldmessage matches that in template - ANY instance replaced
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    
    # rendered reponse returned to client
    # shortcut function
    # first parameter is the template we want to use
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {'boldmessage':'This tutorial has been put together by Andrew McGill.'}
    return render(request, 'rango/about.html', context = context_dict)
