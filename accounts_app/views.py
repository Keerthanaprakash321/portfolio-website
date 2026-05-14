from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Profile, Skill, Education, Experience, Certificate, Training
from .forms import LoginForm, CertificateForm

from projects_app.models import Project

import os
from pathlib import Path

def home(request):
    try:
        profile = Profile.objects.first()
        skills = Skill.objects.all()
        projects = Project.objects.all()
        certificates = Certificate.objects.filter(profile=profile)
        trainings = Training.objects.all()
    except Exception as e:
        profile = None
        skills = []
        projects = []
        certificates = []
        trainings = []
    
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'certificates': certificates,
        'trainings': trainings,
    }
    return render(request, 'accounts_app/home.html', context)



def dashboard(request):
    try:
        # Fetch the admin's profile (first one created)
        profile = Profile.objects.first()
        certificates = Certificate.objects.filter(profile=profile)
        projects = Project.objects.all()
    except Exception:
        profile = None
        certificates = []
        projects = []
    
    return render(request, 'accounts_app/dashboard.html', {
        'owner_profile': profile,
        'certificates': certificates,
        'projects': projects
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.profile = request.user.profile
            certificate.save()
            messages.success(request, 'Certificate added successfully!')
            return redirect('dashboard')
    else:
        form = CertificateForm()
    return render(request, 'accounts_app/certificate_form.html', {'form': form, 'title': 'Add Certificate'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_certificate(request, pk):
    from django.shortcuts import get_object_or_404
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificate updated successfully!')
            return redirect('dashboard')
    else:
        form = CertificateForm(instance=certificate)
    return render(request, 'accounts_app/certificate_form.html', {'form': form, 'title': 'Edit Certificate'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_certificate(request, pk):
    from django.shortcuts import get_object_or_404
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        certificate.delete()
        messages.success(request, 'Certificate deleted successfully!')
        return redirect('dashboard')
    return render(request, 'accounts_app/certificate_confirm_delete.html', {'certificate': certificate})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts_app/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        user_email = request.user.email
        user_name = request.user.username
        
        logout(request)
        
        if user_email:
            try:
                send_mail(
                    subject="Thank You for Visiting",
                    message=f"Hi {user_name},\n\nThank you for visiting my portfolio. I hope to see you again soon!\n\nBest regards,\nKeerthana",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Logout email failed: {e}")

        messages.info(request, "Logged out successfully!")
        return redirect('home')
    return redirect('home')

def certificate_list(request):
    certificates = Certificate.objects.all()
    return render(request, 'accounts_app/certificates.html', {'certificates': certificates})

def resume_view(request):
    return render(request, 'accounts_app/resume.html')

def education_view(request):
    from .models import Profile, Education, Training
    profile = Profile.objects.first()
    education = Education.objects.filter(profile=profile).order_by('-start_date') if profile else []
    trainings = Training.objects.all().order_by('-id')
    return render(request, 'accounts_app/education.html', {'education': education, 'trainings': trainings})
