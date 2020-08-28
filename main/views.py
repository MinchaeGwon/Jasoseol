from django.shortcuts import render, redirect
from .forms import JssForm
from .models import Jasoseol

def home(request):
    all_jss = Jasoseol.objects.all()

    return render(request, 'home.html', {'all_jss':all_jss})

def create(request):
    if request.method == 'POST':
        filled_form = JssForm(request.POST)
        
        if filled_form.is_valid():
            filled_form.save()
            return redirect('home')

    jss_form = JssForm()
    return render(request, 'create.html', {'jss_form':jss_form})
