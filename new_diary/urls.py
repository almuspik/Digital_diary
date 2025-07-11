from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('edit_entry/<str:entry_date>/', views.edit_entry_by_date, name='edit_entry'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
