from django.db import models
from django.contrib.auth.models import User

class Schedule(models.Model):
    # ユーザーとスケジュールを関連付ける
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # スケジュールの日付
    date = models.DateField()
    # 時間（9-18の整数）
    hour = models.IntegerField()
    # 計画の内容
    plan = models.TextField(blank=True)
    # 振り返りの内容
    reflection = models.TextField(blank=True)

    class Meta:
        # ユーザー、日付、時間の組み合わせでユニークに
        unique_together = ('user', 'date', 'hour')