from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
import re
from core.models import Customer  # Ensure this is your correct model import
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        # Retrieving fields from the POST request
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        errors = []

        # Validate username uniqueness
        if User.objects.filter(username=username).exists():
            errors.append("Username is already taken. Please choose another one.")

        # Validate email uniqueness
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered. Please choose another one.")

        # Validate email format
        if '@' not in email:
            errors.append("Invalid email address. Email must contain '@'.")

        # Validate password length and criteria
        if len(password) < 6 or len(password) > 8:
            errors.append("Password must be between 6 and 8 characters long.")
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one letter, one number, and one special character.")

        # Check if password and confirm password match
        if password != confirm_password:
            errors.append("Password and confirm password do not match.")

        # If there are validation errors, return them to the template
        if errors:
            return render(request, 'accounts/regis.html', {'errors': errors})

        # If no errors, create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Create an associated Customer object
        customer = Customer(user=user)
        customer.save()
        # Authenticate and log in the user
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('logn')  # Ensure 'login' matches the name of your login URL

    # Render the registration page for GET requests
    return render(request, 'accounts/regis.html')
    #for login authentication
def login_view(request):
    if request.method == 'POST':
        # Get username and password from POST request
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
  
        # Authenticate the user
        user = authenticate(username=u, password=p)
        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to the index page after login
            return redirect(request.POST.get('next') or '/')  # Replace 'home' with the name of your home view URL pattern
        else:
            # Add an error message for invalid credentials
            messages.error(request, "Login failed, please try again.")
            # Render the same login page with the error message
            return redirect('logn') 
    else:   
    # Render the login page for GET requests or invalid login attempts
        return render(request, 'accounts/logn.html') 
def logout_view(request):
    logout(request)
    return redirect(request.POST.get('next') or '/') # Ensure 'home' matches the name of your home view URL pattern
