from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login-view'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register-view'),
    path('home', views.home, name='home'),
    path('update/<task_id>/<int:step_id>/', views.update, name='update'),
    path('task/<task_id>', views.task, name='task'),
    path('important', views.important, name='important'),
    path('done', views.done, name='done'), 
    path('show', views.show, name='show'), 
    path('show_task/<task_id>', views.show_task, name='show-task'), 
    path('search', views.search_view, name='search'),
    path('groupe', views.groupe, name='groupe'),
]
