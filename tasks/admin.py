from django.contrib import admin
from .models import UserProfile, MasterTask, DailyMission

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_exp', 'rank', 'current_streak']
    search_fields = ['user__username']

@admin.register(MasterTask)
class MasterTaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_name', 'target_hours', 'completed_hours', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'task_name']

@admin.register(DailyMission)
class DailyMissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'master_task', 'date', 'target_minutes', 'completed_minutes', 'is_completed']
    list_filter = ['date', 'is_completed']
    search_fields = ['user__username', 'master_task__task_name']