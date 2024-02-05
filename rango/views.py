from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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
    visitor_cookie_handler(request)
    
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {'boldmessage':'This tutorial has been put together by Andrew McGill.'}
    visitor_cookie_handler(request)
    
    context_dict['visits'] = int(request.session['visits'])
    
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

@login_required
def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST': # case insensitive in form
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            # if valid - save -- referential integrity
            cat = form.save(commit=True)
            print(cat, cat.slug) # printout to console
            
            # reverse is equivalent of the url template tag within python code
            return redirect(reverse('rango:index'))
        
        else:
            # errors
            print(form.errors)
      
    # bad form, new form, no form supplied
    # render w/ error msgs if any        
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    # cannot add a page to a Category that does not exist
    if category is None:
        return redirect(reverse('rango:index'))
    
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

def register(request):
    
    registered = False
    
    if request.method == 'POST':
        # attempt to grab info from raw form info
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # hash
            user.save()
            
            # setting user attribute ourselves so delay save until ready
            # avoids referential integrity error - no foreign key
            profile = profile_form.save(commit=False) 
            profile.user = user
            
            # get from input form and put in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
        
        else:
            # mistakes or something else?
            print(user_form.errors, profile_form.errors)
            
    else:
        # render blank
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request,'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        # returns User obj or None
        
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # bad login details provided
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        # most likely GET
        return render(request, 'rango/login.html')
            
@login_required # decorator function executed first
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
        
    request.session['visits'] = visits
    
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
    
    
    
    
    
    
                
        
    
        
        
    
        
