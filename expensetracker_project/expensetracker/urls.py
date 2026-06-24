from django.urls import path
from . import views

urlpatterns = [
  
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

     path('', views.index, name='index'),
    path('add/', views.add_expense, name='add_expense'),
    path('recent/', views.recent_expenses, name='recent_expense'),
    path('total/<str:period>/', views.total_expenses, name='total_expense'),  
    path('total/<str:period>/<str:total_period>/', views.total_expenses, name='total_expense_full'),
]
