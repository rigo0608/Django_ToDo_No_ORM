from django.urls import path
from . import views

# ----------------------
# URL patterns for the app
# ----------------------
urlpatterns = [
    # Web pages
    path('', views.index, name='index'),           # Homepage / Task list
    path('add/', views.add_page, name='add'),      # Page to add a new task
    path('edit/<int:task_id>/', views.edit_page, name='edit'),  # Page to edit a task

    # API endpoints
    path('api/health/', views.health),                          # Simple health check
    path('api/tasks/', views.api_get_tasks),                   # Get all tasks
    path('api/tasks/<int:task_id>/', views.api_get_task),      # Get single task by id
    path('api/tasks/create/', views.api_create_task),          # Create new task
    path('api/tasks/update/<int:task_id>/', views.api_update_task),  # Update task
    path('api/tasks/delete/<int:task_id>/', views.api_delete_task),  # Delete task
]
