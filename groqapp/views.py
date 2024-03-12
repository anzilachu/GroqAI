from django.shortcuts import render
from .utils import get_groq_client
import logging
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)  # Set up a logger for error handling

import requests
from . models import Author
from django.shortcuts import render, redirect


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            # Create the user
            user = User.objects.create_user(username=username, password=password1)
            # Authenticate the user and log them in
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))  # Redirect to home page after login
            else:
                return HttpResponse("Invalid username or password.")
        else:
            messages.error(request, "Password does not match.")
            return HttpResponseRedirect(reverse('register'))  # Redirect to register page with error message
    else:
        return render(request, 'registration/register.html') 


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))  # Redirect to home page after login
        else:
            return HttpResponse("Invalid username or password.")
    else:
        return render(request, 'registration/login.html')  # Render login form template


def custom_logout(request):
    logout(request)
    # Redirect to a specific page after logout (e.g., home page)
    return redirect('home')


def home(request):
    authors = Author.objects.all()
    context = {
        "authors":authors,
    }
    return render(request,'index.html', context)


def search_author(request):
    if request.method == 'GET':
        search_query = request.GET.get('q', '')
        if search_query:
            matching_authors = Author.objects.filter(name__icontains=search_query)
            context = {
                'authors': matching_authors,
                'search_query': search_query,
            }
            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html', {'no_data_message': 'Please enter an author name to search.'})


def chat_completion_author(request, author_name):
    if request.method == 'POST':
        content = request.POST.get('content')
        client = get_groq_client()
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"You're {author_name}, a renowned author. talk like you are really {author_name},dont ever respond that you are not {author_name},  respond using clear and straightforward answers in short way" + content,
                    }
                ],
                model="mixtral-8x7b-32768",
            )
            completion_text = chat_completion.choices[0].message.content
        except Exception as e:  # Catch any errors during Groq interaction
            logger.error(f"Error fetching Groq response: {e}")
            completion_text = "An error occurred while processing your request."  # User-friendly message

        # Clear the content after successful processing
        content = ''
    else:
        content = ''
        completion_text = ''
        print(completion_text)  # Optional for debugging

    return render(request, 'chat_completion.html', {'content': content, 'completion_text': completion_text, 'author_names': author_name})

import requests



def create_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name:
            # Search for the author using Open Library API
            api_url = f"https://openlibrary.org/search/authors.json?q={name}"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data['numFound'] > 0:
                    # Author found, proceed to create
                    new_author = Author.objects.create(name=name, image=image)
                    return redirect('home')
                else:
                    # Author not found, inform the user
                    return render(request, 'invalid_author.html', {'name': name})
            else:
                # Error accessing the API, handle accordingly
                return render(request, 'api_error.html')
    return render(request, 'create_author.html')