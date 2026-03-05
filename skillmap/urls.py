# from django.urls import path
# from .views import dashboard, take_assessment
# from demo_project.skillmap import views

# urlpatterns = [
#     path('assessment/<int:skill_id>/', take_assessment, name='take_assessment'),
#     path('dashboard/', dashboard, name='dashboard'),
#     path('register/', views.register, name='register'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('assessment/<int:skill_id>/<int:level>/', views.take_assessment, name='take_assessment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/register/', views.register, name='register'),
    path('skill/<int:skill_id>/reset/', views.reset_skill, name='reset_skill'),
    path('history/', views.assessment_history, name='assessment_history'),
    path('attempt/<int:attempt_id>/', views.assessment_result, name='assessment_result'),  # ✅ ADD THIS
    path('role/<int:role_id>/delete/', views.delete_role, name='delete_role'),
    path('assessment-result/<int:attempt_id>/', 
     views.assessment_result, 
     name='assessment_result'),
]