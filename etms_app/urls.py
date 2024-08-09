#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

from django.urls import path
from . import views
urlpatterns = [
    path('', views.login),
    path('signup/', views.signup),  
    path('login', views.login),  
    path('dashboard', views.dashboard),  
    path('mark-completed/<int:id>', views.mark_as_completed),  
    path('account', views.my_account),  
    path('emp-tasks', views.tasks),  
    path('logout/', views.logout),  
    path('update/<int:pk>',views.update),
    path('delete/<int:pk>', views.emp_delete_task),
    

]

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@