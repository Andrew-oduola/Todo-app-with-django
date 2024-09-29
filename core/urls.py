from django.urls import path
from .views import TaskList, TaskDetail, CreateTask, UpdateTask, DeleteTask, CustomLoginView, RegisterPage

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page="login"), name="logout"),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task-detail'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('task-update/<int:pk>', UpdateTask.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteTask.as_view(), name='task-delete'),
    path('register/', RegisterPage.as_view(), name='register'),

    # path('logout/', CustomLogoutView.as_view(), name='logout'),
]