from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person
from .forms import PersonForm, PersonSearchForm

# Create your views here.
def index(request):
    return render(request, 'index.html', name='home')
def about(request):
    return render(request, 'about.html', name='info_about')
def contacts(request):
    return render(request, 'contacts.html', name='contact')
def addTree(request):
    return render(request, 'addTree.html', name="createTree")
def created(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.created_by = request.user
            person.save()
            return redirect('person_detail', pk=person.pk)
    else:
        form = PersonForm()
    return render(request, 'genealogy/person_form.html', {'form':form})