"""salt_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from user_center import views as user

urlpatterns = [
    url(r'^login/', user.web_login),
    url(r'^accounts/login/', user.web_login),
    url(r'^$', user.web_login),
    url(r'^logout/', user.web_logout),
    url(r'^add_token/', user.add_token),
    url(r'^change_passwd/', user.user_change_passwd),
    url(r'^user_add/', user.user_add),
    url(r'^index/', user.index),
    url(r'^user/', user.user_center),
    url(r'^user_manage/', user.user_manage),
    url(r'^user_del/', user.user_del)
]
