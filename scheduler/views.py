from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Schedule
from .forms import ScheduleForm
from datetime import datetime, time

@login_required
def schedule_view(request):
    # POSTリクエストの場合、選択された日付を取得
    if request.method == 'POST':
        date = request.POST.get('date')
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        # GETリクエストの場合、今日の日付を使用
        selected_date = datetime.now().date()

    # 9時から18時までの各時間のスケジュールを取得または作成
    schedules = []
    for hour in range(9, 19):
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
    # 指定されたIDのスケジュールを取得
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == 'POST':
        # フォームにPOSTデータを設定
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        # GET時は既存のスケジュールデータでフォームを初期化
        form = ScheduleForm(instance=schedule)
    return render(request, 'scheduler/edit_schedule.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})