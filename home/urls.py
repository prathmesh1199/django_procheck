from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('',views.index,name="index"),
    path('group_signup',views.gr_signup,name="group_signup"),
    path('group_login',views.gr_login,name="group_login"),
    path('group_logout',views.gr_logout,name="group_logout"),
    path('teacher_logout',views.teacher_logout,name="teacher_logout"),
    path('teacher_login',views.teacher_login,name="teacher_login"),
    path('add_projects',views.add_projects,name="add_projects"),
    path('group_statistics',views.group_statistics,name="group_statistics"),
    path('teacher_statistics',views.teacher_statistics,name="teacher_statistics"),
    path('group_project_page',views.group_project_page,name="group_project_page"),
    path('teacher_project_page',views.teacher_project_page,name="teacher_project_page"),
    path('project_info',views.project_info,name="project_info"),
    path('group_info',views.group_info,name="group_info"),
    path('domain_statistics',views.domain_statistics,name="domain_statistics"),
    path('thrust_statistics',views.thrust_statistics,name="thrust_statistics"),
    
    
   
]
