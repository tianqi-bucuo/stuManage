"""stuManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('classes/', views.classes),
    path('add_class/', views.add_class),
    path('del_class/', views.del_class),
    path('edit_class/', views.edit_class),
    path('students/', views.students),
    path('add_student/', views.add_student),
    path('edit_student/', views.edit_student),
    path('modal_add_class/', views.modal_add_class),
    path('modal_edit_class/', views.modal_edit_class),
    path('modal_add_student/', views.modal_add_student),
    path('modal_edit_student/', views.modal_edit_student),
    path('teachers/', views.teachers),
    path('add_teacher/', views.add_teacher),
    path('edit_teacher/', views.edit_teacher),
    path('get_all_class/', views.get_all_class),
    path('modal_add_teacher/', views.modal_add_teacher),
    path('test/', views.test),
    path('layout/', views.layout),
    path('login/', views.login),

]
