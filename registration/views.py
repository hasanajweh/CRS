from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Course, CourseSchedule
from django.contrib import messages
from django.contrib.auth import logout


# Handles user sign-up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the home page after signup
            return redirect('home')
        else:
            # If the form is not valid, add an error message
            messages.error(request, "There was an error with your signup. Please check your details and try again.")
    else:
        form = SignUpForm()
    # Render the signup page with the form
    
    return render(request, 'registration/signup.html', {'form': form})



# Handles user login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Displays the home page
@login_required
def home(request):
    return render(request, 'registration/home.html')

def custom_logout(request):
    logout(request)
    return redirect('user_login')
# Handles course searching
@login_required
def course_search(request):
    query = request.GET.get('query', '')

    if query:
        courses = Course.objects.filter(
            Q(code__icontains=query) | 
            Q(name__icontains=query) |
            Q(instructor__icontains=query)
        )
    else:
        courses = Course.objects.none()

    return render(request, 'registration/course_search.html', {'courses': courses, 'query': query})

from django.shortcuts import get_object_or_404, render
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'registration/course_detail.html', {'course': course})

def course_schedule(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    schedule = get_object_or_404(CourseSchedule, course=course)
    return render(request, 'registration/course_schedule.html', {'course': course, 'schedule': schedule})


