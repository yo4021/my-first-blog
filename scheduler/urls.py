from django.urls import path
from . import views

urlpatterns = [
    # スケジュール一覧・作成ページ
    path('', views.schedule_view, name='schedule'),
    # スケジュール編集ページ
    path('edit/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    # ユーザー登録ページ
    path('register/', views.register, name='register'),
]