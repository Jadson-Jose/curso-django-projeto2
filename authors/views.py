from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

from authors.templates.authors.forms.login import LoginForm
from authors.templates.authors.forms.register_form import RegisterForm

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse("authors:create"),
    })

def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Your user is create, please login.')
        
        del(request.session['register_form_data'])
    
    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    return render(request, 'authors/pages/login.html')
