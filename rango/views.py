from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # query db for a list of cats
    # order cats by likes in desc order
    # retrieve top 5
    # put into context dict
    # pass to temp engine
    
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list =  Page.objects.order_by('-views')[:5]
    
    
    # boldmessage matches that in template - ANY instance replaced
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list
    
    # rendered reponse returned to client
    # shortcut function
    # first parameter is the template we want to use
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {'boldmessage':'This tutorial has been put together by Andrew McGill.'}
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        
        context_dict['category'] = category # used in temp to verify category exists
    except Category.DoesNotExist:
        # don't do anything - temp will display no category message
        context_dict['category'] = None
        context_dict['pages'] = None
        
    return render(request, 'rango/category.html', context=context_dict)
        
    
        
