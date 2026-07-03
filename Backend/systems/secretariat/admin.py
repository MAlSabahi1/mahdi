from django.contrib import admin
from .models import Correspondence, Task, Circular
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Correspondence)
class CorrespondenceAdmin(SimpleHistoryAdmin):
    list_display = ('reference_number', 'subject', 'type', 'status', 'date', 'sender', 'receiver')
    list_filter = ('type', 'status', 'date')
    search_fields = ('reference_number', 'subject', 'sender', 'receiver')

@admin.register(Task)
class TaskAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description')

@admin.register(Circular)
class CircularAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'date_issued', 'is_active')
    list_filter = ('is_active', 'date_issued')
    search_fields = ('title', 'content')
