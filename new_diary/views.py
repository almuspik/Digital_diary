from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import DiaryEntry, Userprofile
from .forms import DiaryEntryForm, SignUpForm
from django.conf import settings
from datetime import datetime
from django.http import JsonResponse
from django.utils.dateparse import parse_date
import json


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            Userprofile.objects.create(
                user=user,
                phone=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email'],
                dob=form.cleaned_data['date_of_birth']
            )
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('calendar')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def calendar_view(request):
    user = request.user
    dob = user.profile.dob

    # Load all entries to pass to FullCalendar
    entries = DiaryEntry.objects.filter(user=user)
    events = [
        {
            "title": entry.title,
            "start": entry.entry_date.strftime('%Y-%m-%d'),
            "url": f"/edit_entry/{entry.entry_date}/"
        }
        for entry in entries
    ]
    return render(request, 'calendar.html', {
         'form': form,
        'entries': entries,
        'dob': dob,
        'events': json.dumps(events, cls=DjangoJSONEncoder)
    })


@login_required
def edit_entry_by_date(request, entry_date):
    user = request.user
    try:
        entry_date_obj = datetime.strptime(entry_date, "%Y-%m-%d").date()
    except ValueError:
        return redirect("calendar")

    entry, created = DiaryEntry.objects.get_or_create(user=user, entry_date=entry_date_obj)

    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("calendar")
    else:
        form = DiaryEntryForm(instance=entry)

    return render(request, 'edit_entry.html', {
        'form': form,
        'entry_date': entry_date
    })
@login_required
def calendar_view(request):
    user = request.user
    dob = user.profile.dob  # 'profile' matches the related_name

    if request.method == 'POST':
        entry_date = request.POST.get('entry_date')
        try:
            diary_entry = DiaryEntry.objects.get(user=user, entry_date=entry_date)
            form = DiaryEntryForm(request.POST, instance=diary_entry)
        except DiaryEntry.DoesNotExist:
            form = DiaryEntryForm(request.POST)

        if form.is_valid():
            diary_entry = form.save(commit=False)
            diary_entry.user = user
            diary_entry.save()
            return redirect('calendar')
    else:
        date_str = request.GET.get('date')
        if date_str:
            entry_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            entry = DiaryEntry.objects.filter(user=user, entry_date=entry_date).first()
            form = DiaryEntryForm(instance=entry, initial={'entry_date': entry_date})
        else:
            # ✅ Add this line to fix the "form not defined" error
            form = DiaryEntryForm()

    # ✅ Prepare events as JSON for calendar display
    entries = DiaryEntry.objects.filter(user=user)
    events = [
        {"title": "📝 Entry", "start": entry.entry_date.strftime("%Y-%m-%d")}
        for entry in entries
    ]

    return render(request, 'calendar.html', {
        'form': form,
        'entries': entries,
        'dob': dob,
        'events': events,  # Send to JS calendar
    })
