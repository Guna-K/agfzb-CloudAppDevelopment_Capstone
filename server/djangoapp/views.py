from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('index')  # Redirect to the index page or another appropriate page
        else:
            messages.error(request, 'Invalid login credentials.')
    
    return render(request, 'djangoapp/login.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')  # Redirect to the login page or another appropriate page

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # You should add more validation and error handling here
        
        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'You have successfully registered.')
        return redirect('login')  # Redirect to the login page after registration
    
    return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "your-cloud-function-domain/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    # You can add code here to fetch the list of dealerships from your models
    # For example: dealerships = Dealership.objects.all()
    # Pass the dealerships to the template context
    context = {
        'dealerships': dealerships  # Replace 'dealerships' with your actual data
    }
    return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    # You can add code here to fetch dealer details and reviews based on dealer_id
    # For example: dealer = get_object_or_404(Dealership, id=dealer_id)
    # Pass the dealer and reviews to the template context
    context = {
        'dealer': dealer,  # Replace 'dealer' with your actual data
        'reviews': reviews  # Replace 'reviews' with your actual data
    }
    return render(request, 'djangoapp/dealer_details.html', context)

# Create an `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        # Process the review submission and save it to the database
        # You can add code here to validate and save the review
        # After saving, you can redirect to the dealer details page or another appropriate page
        messages.success(request, 'Review submitted successfully.')
        return redirect('dealer_details', dealer_id=dealer_id)  # Redirect to dealer details page

    # Handle GET requests separately if needed
    return render(request, 'djangoapp/add_review.html')
