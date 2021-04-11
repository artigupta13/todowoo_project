"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from todoApp import views

from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    #Auth
    path('signup/',views.signupuser,name='signupuser'),
    path('login/',views.loginuser,name='loginuser'),
    path('logout/',views.logoutuser,name='logoutuser'),

    #todo
    path('',views.home,name='home'),
    path('create/',views.createtodo,name='createtodo'),
    path('current/',views.currenttodos,name='currenttodos'),
    path('completed/',views.completedtodos,name='completedtodos'),
    path('todo/<int:todo_pk>',views.viewtodo,name='viewtodo'),
    path('todo/<int:todo_pk>/complete',views.completetodo,name='completetodo'),
    path('todo/<int:todo_pk>/delete',views.deletetodo,name='deletetodo'),

    path('password_reset/', views.password_reset, name='password_reset'),
    #url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #auth_views.password_reset_confirm, name='password_reset_confirm'),
    #url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


]
