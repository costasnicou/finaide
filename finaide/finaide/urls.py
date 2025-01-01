"""
URL configuration for finaide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker import views
from tracker.views import CustomLoginView

# from tracker import views.CustomLoginView


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage' ),
    path('tracker/', include('tracker.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
    # path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
