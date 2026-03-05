# missions/tasks/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
    """ユーザープロフィール - 経験値や称号を管理"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_exp = models.IntegerField(default=0, verbose_name='累計経験値')
    rank = models.CharField(max_length=20, default='Iron', verbose_name='称号')
    current_streak = models.IntegerField(default=0, verbose_name='現在の継続日数')
    max_streak = models.IntegerField(default=0, verbose_name='最高継続日数')
    last_activity_date = models.DateField(null=True, blank=True, verbose_name='最終活動日')
    
    def __str__(self):
        return f"{self.user.username}のプロフィール"
    
    class Meta:
        verbose_name = 'ユーザープロフィール'
        verbose_name_plural = 'ユーザープロフィール'


class MasterTask(models.Model):
    """マスタータスク - 長期目標を管理"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    task_name = models.CharField(max_length=100, verbose_name='タスク名')
    target_hours = models.IntegerField(verbose_name='目標時間（分）')
    completed_hours = models.IntegerField(default=0, verbose_name='達成時間（分）')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    
    def __str__(self):
        return f"{self.user.username} - {self.task_name}"
    
    @property
    def progress_percentage(self):
        """進捗率を計算"""
        if self.target_hours == 0:
            return 0
        return (self.completed_hours / self.target_hours) * 100
    
    class Meta:
        verbose_name = 'マスタータスク'
        verbose_name_plural = 'マスタータスク'
        ordering = ['-created_at']  # 新しい順


class DailyMission(models.Model):
    """デイリーミッション - 日々のタスクを管理"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    master_task = models.ForeignKey(
        MasterTask, 
        on_delete=models.CASCADE, 
        verbose_name='マスタータスク'
    )
    target_minutes = models.IntegerField(verbose_name='目標時間（分）')
    completed_minutes = models.IntegerField(default=0, verbose_name='達成時間（分）')
    date = models.DateField(default=date.today, verbose_name='日付')
    is_completed = models.BooleanField(default=False, verbose_name='完了フラグ')
    
    def __str__(self):
        return f"{self.user.username} - {self.master_task.task_name} ({self.date})"
    
    def complete(self):
        """ミッション完了処理"""
        self.is_completed = True
        self.save()
        
        # マスタータスクの進捗を更新
        self.master_task.completed_hours += self.completed_minutes
        self.master_task.save()
        
        # 経験値を加算
        exp_gained = self.completed_minutes * 10
        self.user.profile.total_exp += exp_gained
        self.user.profile.save()
    
    class Meta:
        verbose_name = 'デイリーミッション'
        verbose_name_plural = 'デイリーミッション'
        unique_together = ['user', 'master_task', 'date']  # 同日同タスクは1つまで
        ordering = ['-date']