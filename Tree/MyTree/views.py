from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html', name='home')
def about(request):
    return render(request, 'about.html', name='info_about')
def contacts(request):
    return render(request, 'contacts.html', name='contact')
def addTree(request):
    return render(request, 'addTree.html', name="createTree")
