from django.shortcuts import render , redirect , reverse
from .forms import LoginForm , RegisterForm
from django.contrib.auth import authenticate , login , get_user_model , logout

User = get_user_model()

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    login_form = LoginForm(request.POST or None)
    context = {
        "login_form" : login_form
    }
    if login_form.is_valid():
        context["form"] = LoginForm
        user = authenticate(username = login_form.cleaned_data.get("username") , password = login_form.cleaned_data.get("password"))
        if user is not None:
            login(request , user)
            return redirect("/?message=You+are+loggedin+successfully")
        else:
            context["error"] = "Username or Password is not correct"
    
    return render(request , 'accounts/login.html' , context)

def register_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    register_form = RegisterForm(request.POST or None)
    context = {
        "register_form" : register_form
    }
    if register_form.is_valid():
        context["form"] = RegisterForm()
        User.objects.create_user(username = register_form.cleaned_data.get("username") , password = register_form.cleaned_data.get("password") , email = register_form.cleaned_data.get("email"))
        return redirect(reverse("accounts:login"))

    return render(request , 'accounts/register.html' , context)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/?message=You+are+loggedout+successfully')
    return redirect('/')
