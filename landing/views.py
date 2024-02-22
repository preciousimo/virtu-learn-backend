from django.shortcuts import render, redirect
from landing.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from landing.models import User

# Create your views here.
def landing(request):
    return render(request, 'landing/landing.html')

def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=True)
            username = form.cleaned_data['username']
            messages.success(request, f"New Account Created: {username}.")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('/')
    else:
        form =  UserRegisterForm()

    context = {'form': form}
    return render(request, "accounts/signup.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {email}. You are now logged in.")
                return redirect('/')
            else:
                messages.warning(request, "Incorrect password.")
                
        except User.DoesNotExist:
            messages.warning(request, f'A user with the email {email} does not exist. Create an account.')

    return render(request, 'accounts/login.html')

def logout(request):

    logout(request)
    messages.info(request, "You have successfully logged out.") 

    return redirect('login')