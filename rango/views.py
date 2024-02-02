from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST': # case insensitive in form
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            # if valid - save -- referential integrity
            cat = form.save(commit=True)
            print(cat, cat.slug) # printout to console
            
            return redirect('/rango/')
        
        else:
            # errors
            print(form.errors)
      
    # bad form, new form, no form supplied
    # render w/ error msgs if any        
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    # cannot add a page to a Category that does not exist
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid(): # data submitted - return to show cat 
            if category: # belt and braces?
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
                
        
    
        
        
    
        
