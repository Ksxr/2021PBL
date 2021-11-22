"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
<<<<<<< HEAD
from django.contrib.auth.views import LogoutView
from moticom import views

=======
from django.contrib.auth import views as auth_views
>>>>>>> 738d15127f96309cee2e66ad2716bf89bea35d60

urlpatterns = [
    #path('moticom/',include('moticom.urls')),
    path('accounts/', include('django.contrib.auth.urls')),    # 追加
    path('accounts/password_change_form/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change_form'),    # 追加
    path('accounts/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_finish.html'), name='password_change_done'), # 追加
    path('moticom/',include('moticom.urls')),
#    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('login', views.login.as_view(), name='login'),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.signup),
=======
    #path('', include('django.contrib.auth.urls')),# これを追加
    
>>>>>>> 738d15127f96309cee2e66ad2716bf89bea35d60
]

#from django.contrib import admin
#from django.urls import include, path
#from django.contrib.auth.views import LogoutView
#from moticom import views


#urlpatterns = [
#    path('moticom/',include('moticom.urls')),
#    path('polls/', include('polls.urls')),
#    path('admin/', admin.site.urls),
#    path('login', views.login.as_view(), name='login'),
#    path('logout/', LogoutView.as_view()),
#    path('signup/', views.signup),
#]