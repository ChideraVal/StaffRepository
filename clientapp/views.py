from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Loan, Staff, StaffFile
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomAuthForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, LoanForm, StaffForm, StaffFileForm, EditStaffForm, EditStaffFileForm
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

# @login_required
# def home(request):
#     loans = Loan.objects.filter(owner=request.user).all()
#     return render(request, 'home.html', {'loans': loans, 'total': sum([i.amount_with_tax() for i in loans])})

@login_required
def home(request):
    profiles = Staff.objects.all()
    return render(request, 'dashboard.html', {'profiles': profiles})

@login_required
def profile_details(request, id):
    profile = Staff.objects.get(id=id)
    return render(request, 'profiledetails.html', {'profile': profile})

@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def request_loan(request):
    if request.method == 'POST':
        form = LoanForm(data=request.POST)
        if form.is_valid():
            new_loan = form.save(owner=request.user)
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'editprofile.html', {'form': form})
    form = LoanForm()
    return render(request, 'requestloan.html', {'form': form})

@login_required
def create_new_profile(request):
    if request.method == 'POST':
        form = StaffForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'createprofile.html', {'form': form})
    form = StaffForm()
    return render(request, 'createprofile.html', {'form': form})

@login_required
def edit_staff(request, id):
    profile = Staff.objects.get(id=id)
    if request.method == 'POST':
        form = EditStaffForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'/profiledetails/{id}/')
        else:
            print(form.errors)
            return render(request, 'editstaff.html', {'form': form, 'profile': profile})
    form = EditStaffForm(instance=profile)
    return render(request, 'editstaff.html', {'form': form, 'profile': profile})

@login_required
def delete_staff(request, id):
    profile = Staff.objects.get(id=id)
    if request.method == 'POST':
        profile.delete()
        return redirect('/')
    return render(request, 'deletestaff.html', {'profile': profile})

@login_required
def delete_file(request, id):
    file = StaffFile.objects.get(id=id)
    owner_id = file.staff.id
    if request.method == 'POST':
        file.delete()
        return redirect(f'/profiledetails/{owner_id}/')
    return render(request, 'deletefile.html', {'file': file})

@login_required
def edit_file(request, id):
    file = StaffFile.objects.get(id=id)
    if request.method == 'POST':
        form = EditStaffFileForm(instance=file, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'/profiledetails/{file.staff.id}/')
        else:
            print(form.errors)
            return render(request, 'editfile.html', {'form': form, 'file': file})
    form = EditStaffFileForm(instance=file)
    return render(request, 'editfile.html', {'form': form, 'file': file})

@login_required
def create_new_file(request, id):
    profile = Staff.objects.get(id=id)
    if request.method == 'POST':
        form = StaffFileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(staff=profile)
            return redirect(f'/profiledetails/{id}/')
        else:
            print(form.errors)
            return render(request, 'createfile.html', {'form': form, 'profile': profile})
    form = StaffFileForm()
    return render(request, 'createfile.html', {'form': form, 'profile': profile})

def sign_in(request):
    path = request.get_full_path()
    next_url = path.replace('/signin/?next=', '')
    logging.info(f'PATH = {path}')
    logging.info(f'NEXT = {next_url}')
    print(f"COOKIES: {request.COOKIES}")

    if request.method == 'POST':
        form = CustomAuthForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next_url == '/signin/':
                return redirect('/')
            return redirect(next_url)
        else:
            print(form.errors)
            return render(request, 'signin.html', {'form': form, 'path': path})
    form = CustomAuthForm(request)
    return render(request, 'signin.html', {'form': form, 'path': path})

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/signin/')
        else:
            print(form.errors)
            return render(request, 'signup.html', {'form': form})
    form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'editprofile.html', {'form': form})
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'editprofile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'changepassword.html', {'form': form})
    form = PasswordChangeForm(user=request.user)
    return render(request, 'changepassword.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('/signin/')