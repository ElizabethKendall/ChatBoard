from __future__ import unicode_literals
from django.shortcuts import render, reverse, redirect
from forms import RegistrationForm, RegisterForm, SignInForm, SignIn_Form, UpdateInfoForm, UpdateInfo_Form, UpdateInfoAdminForm, UpdateInfoAdmin_Form, UpdatePasswordForm, UpdatePassword_Form, UpdateDescription_Form
from .models import User
from django.contrib import messages 

# Create your views here.
def index(request):
    return render(request, "user_app/index.html")

# To create a new record, first render the register.html page. Then call the create route, which redirects to a landing page route, such as users:index.
def register(request):
    context = {
        'myregistrationform': RegistrationForm()
    }    
    return render(request, "user_app/register.html", context)
def new(request):
    context = {
        'myregistrationform': RegistrationForm()
    }    
    return render(request, "user_app/new.html", context)
def create(request):
    # this is the method that actually creates a user who is registering itself, or who is being registered by an admin
    if request.method == "POST":
        bound_form = RegisterForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            users = User.objects.all()
            if len(users) == 1:
                users[0].user_level = 9
                users[0].save()
            else:
                users[0].first_name, users[0].last_name
            user = User.objects.get(email=request.POST['email'], password=request.POST['password'])
            if "user_id" not in request.session:
                request.session['user_id'] = user.id
                request.session['user_level'] = user.user_level
            if request.session['user_level'] >= 9:
                return redirect(reverse("users:dashboard_admin")) 
            else:
                return redirect(reverse("users:dashboard")) 
        else:
            context = {
                'myregistrationform': bound_form
            }
            return render(request, "user_app/register.html", context) 
def sign_in(request):
    context = {
        'mysigninform': SignInForm()
    }    
    return render(request, "user_app/signin.html", context)
def verify_sign_in(request):
    if request.method == "POST":
        bound_form = SignIn_Form(request.POST)
        if bound_form.is_valid():
            # errors should be checked for elsewhere with validator methods in models.py and forms.py. Thus, using get instead of filter here.
            user = User.objects.get(email=request.POST['email'], password=request.POST['password'])
            request.session['user_id'] = user.id
            request.session['user_level'] = user.user_level
            if request.session['user_level'] >= 9:
                return redirect(reverse("users:dashboard_admin")) 
            else:
                return redirect(reverse("users:dashboard")) 
        else: 
            context = {
                'mysigninform': bound_form
            }
            return render(request, "user_app/signin.html", context)       

def log_out(request):
    request.session.clear()
    return redirect(reverse("users:index")) 

def edit(request):
    user =  User.objects.get(id=request.session['user_id'])
    print request.session['user_id']
    myupdateinfoform = UpdateInfo_Form(instance=user)
    myupdatepasswordform = UpdatePasswordForm()
    myupdatedescriptionform = UpdateDescription_Form(instance=user)
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'myupdateinfoform': myupdateinfoform,
        'myupdatepasswordform': myupdatepasswordform, 
        'myupdatedescriptionform':myupdatedescriptionform
    }
    return render(request, "user_app/edit.html", context)
def edit_admin(request, number):
    user =  User.objects.get(id=number)
    myupdateinfoform = UpdateInfoAdmin_Form(instance=user)
    myupdatepasswordform = UpdatePasswordForm()
    myupdatedescriptionform = UpdateDescription_Form(instance=user)
    context = {
        'user':User.objects.get(id=number),
        'myupdateinfoform': myupdateinfoform,
        'myupdatepasswordform': myupdatepasswordform, 
        'myupdatedescriptionform':myupdatedescriptionform
    }
    return render(request, "user_app/edit_admin.html", context)
def update_my_info(request, number):
    if request.session['user_level']>=9 or request.session['user_id'] == number:
        if request.method == "POST":
            user = User.objects.get(id=number)
            my_bound_form = UpdateInfo_Form(request.POST, instance=user)

            if my_bound_form.is_valid():
                my_bound_form.save()
                context = {
                    'users':User.objects.all()
                }
                return render(request, "user_app/dashboard_admin.html", context)
            else:
                print "*USER APP BOUND FORMS*"*10                
                print my_bound_form
                print "*USER APP BOUND FORMS*"*10                
                context = {
                    'user': user,
                    'myupdateinfoform': my_bound_form,
                    'myupdatepasswordform': UpdatePasswordForm(), 
                    'myupdatedescriptionform':UpdateDescription_Form(instance=user)
                }
                return render(request, "user_app/edit_admin.html", context)
    else:
        context = {
            'users':User.objects.all()
        }
        return render(request, "user_app/dashboard.html", context) 
def update_my_description(request, number):
    if request.session['user_level']>=9 or request.session.user_id == number:
        if request.method == "POST":
            user = User.objects.get(id=number)
            my_bound_form = UpdateDescription_Form(request.POST, instance=user)
            if my_bound_form.is_valid():
                my_bound_form.save()
                context = {
                    'users':User.objects.all()
                }
                return render(request, "user_app/dashboard_admin.html", context)
            else:                 
                context = {
                    'user': user,
                    'myupdateinfoform': UpdateInfo_Form(instance=user),
                    'myupdatepasswordform': UpdatePasswordForm(), 
                    'myupdatedescriptionform':my_bound_form
                }
                return render(request, "user_app/edit_admin.html", context)
    else:
        context = {
            'users':User.objects.all()
        }
        return render(request, "user_app/dashboard.html", context)
def update_my_password(request, number):
    if request.method == "POST":
        user = User.objects.get(id=number)
        my_bound_form = UpdatePassword_Form(request.POST, instance=user)
        if my_bound_form.is_valid():
            my_bound_form.save()   
            context = {
                'users':User.objects.all()
            }
            return render(request, "user_app/dashboard_admin.html", context)
        else:                 
            context = {
                'user': user,
                'myupdateinfoform': UpdateInfo_Form(instance=user),
                'myupdatepasswordform': my_bound_form, 
                'myupdatedescriptionform':UpdateDescription_Form(instance=user)
            }
            return render(request, "user_app/edit_admin.html", context)
    else:
        context = {
            'users':User.objects.all()
        }
        return render(request, "user_app/dashboard.html", context)

def delete(request, number):
    if request.session['user_level'] >=9:
        if number != "17" and number != "18" and number != "19" and number != "20":
            User.objects.get(id=number).delete()
    context = {
        'users':User.objects.all()
    }
    return render(request, "user_app/dashboard_admin.html", context)

def dashboard(request):
    context = {
        'users':User.objects.all()
    }
    return render(request, "user_app/dashboard.html", context)
def dashboard_admin(request):
    context = {
        'users':User.objects.all()
    }
    return render(request, "user_app/dashboard_admin.html", context)

def show(request, number):
    return render(request, "msg_app/messages.html")