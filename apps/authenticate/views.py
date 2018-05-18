from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse
from .forms import UserForm
from .models import User
import bcrypt

def index(request):
 
    if request.method == 'GET':
        if 'user' in request.session:
            return redirect(reverse('auth:success'))
        return render(request, 'authenticate/index.html', { 'form' : UserForm() })
                
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        errors = User.objects.validate(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('auth:index'))
        else:
            user = form.save(commit=False)
            user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
            user.save()
            request.session['user'] = '{} {}'.format(user.first_name, user.last_name)
            messages.success(request, 'Successfully registerd and logged in.')            
            return redirect(reverse('auth:success'))                 

def login(request):

    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.filter(email = email).first()

    if user:
        valid_pw = bcrypt.checkpw(password.encode(), user.password.encode())
        if valid_pw:
            request.session['user'] = '{} {}'.format(user.first_name, user.last_name)
            messages.success(request, 'Successfully registerd and logged in.')             
            return redirect(reverse('auth:success'))
        else:
            messages.error(request, 'Invalid user/password')
            return redirect(reverse('auth:index'))                            
    else:
        messages.error(request, 'User does not exist')
        return redirect(reverse('auth:index'))        
    
                   
def success(request):

    return render(request, 'authenticate/success.html')
    

def logout(request):           

    user = request.session['user']             
    request.session.clear()
    messages.success(request, '{} has been logged out'.format(user))
    return redirect(reverse('auth:index'))
