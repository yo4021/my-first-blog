from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Schedule
from .forms import ScheduleForm
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('schedule')
        else:
            return render(request, 'registration/login.html', {'error': 'ユーザー名またはパスワードが正しくありません。'})
    return render(request, 'registration/login.html')

@login_required
def schedule_view(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        selected_date = request.GET.get('date')
        if selected_date:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        else:
            selected_date = datetime.now().date()

    schedules = []
    for hour in range(24):
        schedule, created = Schedule.objects.get_or_create(
            user=request.user,
            date=selected_date,
            hour=hour
        )
        schedules.append(schedule)

    return render(request, 'scheduler/schedule.html', {
        'schedules': schedules,
        'selected_date': selected_date
    })

@login_required
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, user=request.user)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect(f'/schedule/?date={schedule.date}')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'scheduler/edit_schedule.html', {'form': form, 'schedule': schedule})

@login_required
def clear_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, user=request.user)
    schedule.plan = ''
    schedule.reflection = ''
    schedule.save()
    return redirect(f'/schedule/?date={schedule.date}')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})