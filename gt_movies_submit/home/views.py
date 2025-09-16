from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', {'template_data': {'title':'Home'}})

def about(request):
    return render(request, 'home/about.html', {'template_data': {'title':'About'}})
