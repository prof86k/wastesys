import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msg
from datetime import datetime

# from django.views.generic import CreateView
from . import models as mdl
from . import forms as fms
from waste import models as wdl


# Create your views here.
def user_account_creation(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ user registration view
    passwaord:waste2022
    '''
    if request.method == 'POST':
        form = fms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_login')
    else:
        form = fms.UserRegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_login(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ user login view
    '''
    if request.method == "POST":
        form = fms.UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.admin:
                    return redirect('accounts:dashboard')
                else:
                    return redirect('accounts:user_dashboard')
            else:
                msg.error(request, 'No User found')
    else:
        form = fms.UserLoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def dashboard(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ admin user dashboard view
    '''
    number_of_users = mdl.User.objects.filter(staff=True, admin=True).count()
    number_of_admin = mdl.User.objects.filter(admin=True).count()
    total_wastes = wdl.DustBin.objects.filter(
        bin_collected=True, payment_made=True).count()
    new_wastes = wdl.DustBin.objects.filter(bin_ready=True).count()
    paid_wastes = wdl.DustBin.objects.filter(payment_made=True).count()
    unpaid_wastes = wdl.DustBin.objects.filter(
        bin_collected=False, payment_made=False).count()
    wastes = wdl.DustBin.objects.order_by('-date_created').all()
    places = wdl.WasteLocation.objects.order_by('-date_created').all()
    places_covered = wdl.WasteLocation.objects.count()
    waste_type_covered = wdl.WasteType.objects.count()
    context = {
        'wastes': wastes,
        'places': places,
        'number_of_users': number_of_users,
        'number_of_admin': number_of_admin,
        'total_wastes': total_wastes,
        'places_covered': places_covered,
        'waste_type_covered': waste_type_covered,
        'new_wastes': new_wastes,
        'paid_wastes': paid_wastes,
        'unpaid_wastes': unpaid_wastes,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def users_dashboard(request: HttpRequest, *agrs, **kwargs) -> HttpResponse:
    '''
    @ users dasboad
    '''
    my_disposed_waste = wdl.DustBin.objects.filter(user=request.user).count()
    paid = wdl.DustBin.objects.filter(
        user=request.user, payment_made=True).count()
    unpaid_wastes = wdl.DustBin.objects.filter(
        bin_collected=False, payment_made=False).count()
    wastes = wdl.DustBin.objects.order_by(
        '-date_created').filter(user=request.user).all()

    context = {
        'my_disposed_waste': my_disposed_waste,
        'paid': paid, 'unpaid_wastes': unpaid_wastes,
        'wastes': wastes, 'today': datetime.date(datetime.today()),
    }
    return render(request, 'accounts/user_dashboard.html', context)


def profile(request: HttpRequest, user_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ user profile view
    '''
    user = get_object_or_404(mdl.User, id=user_id)
    admin_user = get_object_or_404(mdl.User, id=user_id)
    if (admin_user.admin) or (request.user == user):
        user_profile_info = mdl.UserProfile.objects.filter(user=user).first()
        if user_profile_info is not None:
            form = fms.UserProfileForm(
                instance=user_profile_info, data=request.POST, files=request.FILES)
        else:
            form = fms.UserProfileForm(instance=user_profile_info)

    context = {
        'user_profile_info': user_profile_info,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)


def update_profile(request: HttpRequest, user_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ update user profile
    '''
    user = get_object_or_404(mdl.User, id=user_id)
    admin_user = get_object_or_404(mdl.User, id=user_id)
    if (admin_user.admin) or (request.user == user):
        if request.method == 'POST':
            user_profile_info = mdl.UserProfile.objects.filter(
                user=user).first()
            if not user_profile_info:
                form = fms.UserProfileForm(
                    data=request.POST, files=request.FILES)
                if form.is_valid():
                    print(form.errors)
                    new_profile = form.save(commit=False)
                    new_profile.user = user
                    new_profile.profile_pic = form.cleaned_data.get(
                        'profile_pic')
                    new_profile.save()
                    return redirect('accounts:profile', user_id=user_id)
            form = fms.UserProfileForm(
                instance=user_profile_info, data=request.POST, files=request.FILES)
            if form.is_valid():
                update_user = form.save(commit=False)
                update_user.user = user
                update_user.save()
                return redirect('accounts:profile', user_id=user_id)


def display_all_users(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ show all system users to the super admin
    '''
    users = mdl.User.objects.order_by('-date_joined').all()
    context = {'users': users}
    return render(request, 'accounts/all_users.html', context)


def delete_user_account(request: HttpRequest, user_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ delete user accounts,
    @ only supper admins can delete a staff account or other superusers
    '''
    admin_user = get_object_or_404(mdl.User, email=request.user.email)
    if admin_user.admin:
        try:
            user = get_object_or_404(mdl.User, id=user_id)
            user.delete()
            msg.success(request, 'Account Record Deleted successfully.')
            return redirect('accounts:show_users')
        except Exception as e:
            msg.error(request, 'Unable to delete this user account')
    return redirect('accounts:show_users')


def user_logout(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ logout the current user
    '''
    logout(request)
    msg.info(request, 'Logout Successfull')
    return redirect('accounts:user_login')
