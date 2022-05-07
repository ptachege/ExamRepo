from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist

from Lux.models import Exams
from .forms import *


def index(request):
    try:
        this_user = UserProfile.objects.get(user=request.user)
        return redirect('Lux:dashboard')
    except ObjectDoesNotExist:
        return redirect('Lux:user_create_profile')


def dashboard(request):
    total_users = User.objects.all().count()
    total_papers = Exams.objects.all().count()
    all_papers = Exams.objects.all()
    current_user_profile = UserProfile.objects.get(user=request.user)
    course_taking = current_user_profile.course_taking
    current_year = current_user_profile.current_year

    suggested_for_you = Exams.objects.filter(
        course_name=course_taking, unit_year=current_year, is_validate=True)[:10]
    suggested_for_you_count = Exams.objects.filter(
        course_name=course_taking, unit_year=current_year, is_validate=True).count()
    my_contributions = Exams.objects.filter(
        is_validate=True, user=request.user).count()

    visitor_count = current_user_profile.visitorcount

    context = {
        'total_users': total_users,
        'total_papers': total_papers,
        'all_papers': all_papers,
        'suggested_for_you': suggested_for_you,
        'suggested_for_you_count': suggested_for_you_count,
        'my_contributions': my_contributions,
        'visitor_count': visitor_count,
    }

    current_user_profile.visitorcount = + 1
    current_user_profile.save()

    return render(request, 'Lux/dashboard.html', context)


def all_exams(request):
    all_exams = Exams.objects.filter(is_validate=True)
    context = {
        'all_exams': all_exams
    }

    return render(request, 'Lux/exam_list.html', context)


def suggested_for_you(request):
    current_profile = UserProfile.objects.get(user=request.user)
    course_taking = current_profile.course_taking
    current_year = current_profile.current_year
    suggested_for_you = Exams.objects.filter(
        course_name=course_taking, unit_year=current_year,  is_validate=True)[:10]

    context = {
        'current_profile': current_profile,
        'suggested_for_you': suggested_for_you,
        'count': 0,
    }
    return render(request, 'Lux/suggested_for_you.html', context)


def moi_university_exams(request):
    all_exams = Exams.objects.filter(university='Moi', is_validate=True)
    context = {
        'all_exams': all_exams
    }
    return render(request, 'Lux/moi_university_exams.html', context)


def tuk_university_exams(request):
    all_exams = Exams.objects.filter(university='Tuk', is_validate=True)
    context = {
        'all_exams': all_exams
    }
    return render(request, 'Lux/tuk_university_exams.html', context)


def user_create_profile(request):
    if request.method == 'GET':
        return render(request, 'Lux/create_profile.html')

    if request.method == 'POST':
        form = UserProfileForm(request.POST or None, request.FILES)
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        university = form.data['university']
        campus = form.data['campus']
        current_year = form.data['semester']
        course_taking = form.data['course_taking']
        avatar = request.FILES['avatar']

        UserProfile.objects.create(
            user=request.user,
            university=university,
            campus=campus,
            current_year=current_year,
            course_taking=course_taking,
            avatar=avatar,

        )

        # if successfull, update user model instance.

        current_user = User.objects.get(id=request.user.id)
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = current_user.username
        current_user.save()

        # messages.success(request, 'Profile created successfully')
        return redirect('Lux:welcome')

        print(form.errors)
        messages.warning(request, 'Sorry an error occured')
        return redirect('Lux:user_create_profile')


def edit_profile(request):
    if request.method == 'GET':
        user_profile_detail = UserProfile.objects.get(user=request.user)
        user_detail = User.objects.get(id=request.user.id)

        form = UserProfileForm(instance=user_profile_detail)
        context = {
            'form': form,
            'user_profile_detail': user_profile_detail,
            'user_detail': user_detail,
        }
        return render(request, 'Lux/edit_profile.html', context)


def welcome(request):
    return render(request, 'Lux/welcome.html')


def view_user_profile(request):
    current_user = User.objects.get(id=request.user.pk)
    current_profile = UserProfile.objects.get(user=request.user)
    context = {
        'current_user': current_user,
        'current_profile': current_profile,
    }
    return render(request, 'Lux/user_profile.html', context)


def upload_papers(request):
    if request.method == 'GET':
        my_contributions = Exams.objects.filter(user=request.user)
        context = {
            'my_contributions': my_contributions
        }
        return render(request, 'Lux/upload_papers.html', context)

    if request.method == 'POST':
        form = ExamsForms(request.POST or None, request.FILES)
        university = form.data['university']
        course_name = form.data['course_name']
        unit_name = form.data['unit_name']
        unit_year = form.data['unit_year']
        unit_code = form.data['unit_code']
        unit_file = request.FILES['unit_file']
        exam_year = form.data['exam_year']

        user = request.user
        # save to database
        Exams.objects.create(
            user=user,
            university=university,
            course_name=course_name,
            unit_name=unit_name,
            unit_year=unit_year,
            unit_code=unit_code,
            unit_file=unit_file,
            exam_year=exam_year,
        )
        # if successfull redirect
        messages.success(
            request, 'Upload successful, Content will be reviewed before verification.')
        return redirect('Lux:dashboard')


def pending_approve_papers(request):
    pending_papers = Exams.objects.filter(is_validate=False)
    approved_papers = Exams.objects.filter(is_validate=True)

    context = {
        'pending_papers': pending_papers,
        'approved_papers': approved_papers,
    }
    return render(request, 'Lux/approve_papers.html', context)


# approve a given paper.
def approve_paper(request, pk):
    exam_paper = Exams.objects.get(id=pk)
    exam_paper.is_validate = not exam_paper.is_validate
    exam_paper.save()
    return redirect('Lux:pending_approve_papers')


# chat page
def chat(request):
    if request.method == 'GET':
        all_chats = Chat.objects.all()
        context = {
            'all_chats': all_chats,
        }
        return render(request, 'Lux/chat.html', context)
    if request.method == 'POST':
        message = request.POST.get('message')
        user = request.user

        Chat.objects.create(
            user=user,
            message=message,
        )
        return redirect('Lux:chat')


# manage users
def manage_users(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users
    }
    return render(request, 'Lux/manage_users.html', context)


# block user
def block_user(request, pk):
    this_user = User.objects.get(id=pk)
    this_user.is_active = not this_user.is_active
    this_user.save()

    if this_user.is_active == False:
        messages.success(request, 'Account for ' + this_user.first_name +
                         ' Blocked successfully')
    else:
        messages.success(request, 'Account for ' + this_user.first_name +
                         ' Unlocked successfully')
    return redirect('Lux:manage_users')


def view_userprofile(request, pk):
    try:
        this_user = User.objects.get(id=pk)
        this_user_profile = UserProfile.objects.get(user=this_user)

        context = {
            'current_user': this_user,
            'current_profile': this_user_profile,
        }
        return render(request, 'Lux/user_profile.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, 'This user does not have a profile')
        return redirect('Lux:manage_users')


# this are api calls functions


@api_view(['GET'])
def all_exams_api(request):
    all_exams_qs = Exams.objects.all()
    serializer = AllExamsSerialzer(all_exams_qs, many=True)
    return Response(serializer.data)


# This is authentication process going downward


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(
                    request, 'Logged in Successfully as ' + request.user.username)
                return redirect('Lux:index')
            else:
                messages.warning(request, 'Account not activated')
                return render(request, 'Lux/login.html')
        else:
            messages.warning(request, 'Invalid Username or Password!')
            return render(request, 'Lux/login.html')
    return render(request, 'Lux/login.html')


def logout_user(request):
    logout(request)
    form = UserLogForm(request.POST or None)
    context = {
        'form': form
    }
    messages.success(request, 'Successfully Logged out.')
    return redirect('Lux:login_user')


# user registration function
def register(request):
    if request.method == 'POST':
        form = UserLogForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('Lux:user_create_profile')
        context = {
            'form': form,
        }
        print(form.errors)
        messages.warning(request, 'Error. Username already Taken Try another.')
        return render(request, 'Lux/register.html', context)
    else:
        form = UserLogForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'Lux/register.html', context)
