from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # pass to template engine as context
    # boldmessage matches that in template - ANY instance replaced
    context_dict = {'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}
    
    # rendered reponse returned to client
    # shortcut function
    # first parameter is the template we want to use
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    return HttpResponse('Rango says here is the about page. <a href="/rango/">Index</a>')
