from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Course, CourseSchedule, CustomUser
from django.contrib import messages
from django.db.models import Q
from .models import Course, CourseSchedule, StudentRegistration, Student
#  user sign-up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('thank_you')  
        else:
            messages.error(request, "There was an error with your signup. Please check your details and try again.")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


#  user login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# home page
@login_required
def home(request):
    return render(request, 'registration/home.html')

# Logout user
def custom_logout(request):
    logout(request)
    return redirect('user_login')

# course searching
@login_required
def course_search(request):
    query = request.GET.get('query', '')
    if query:
        courses = Course.objects.filter(Q(code__icontains=query) | Q(name__icontains=query) | Q(instructor__icontains=query))
    else:
        courses = Course.objects.none()
    return render(request, 'registration/course_search.html', {'courses': courses, 'query': query})

# course detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Calculate the number of available spots if not stored in the database
    spots_taken = StudentRegistration.objects.filter(course=course).count()
    available_spots = course.capacity - spots_taken
    context = {
        'course': course,
        'available_spots': available_spots,
        
    }
    return render(request, 'registration/course_detail.html', context)


# course schedule
def course_schedule(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    schedule = get_object_or_404(CourseSchedule, course=course)
    # Assuming that available spots are calculated in the same way as in course_detail view
    spots_taken = StudentRegistration.objects.filter(course=course).count()
    available_spots = course.capacity - spots_taken
    context = {
        'course': course,
        'schedule': schedule,
        'available_spots': available_spots,
    }
    return render(request, 'registration/course_schedule.html', context)


def thank_you(request):
    return render(request, 'thank_you.html')


