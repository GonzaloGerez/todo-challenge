from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('tasks/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/status/', views.update_task_status, name='update_task_status'),
    path('tasks/search/', views.search_tasks, name='search_tasks'),
]

