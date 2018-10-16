# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def web_login(requests):
    if requests.method == "POST":
        username = requests.POST['username']
        password = requests.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(requests, user)
            return render(requests, 'index/')
        else:
            messages.error(requests, '用户名或密码错误')
            return render(requests, 'login.html')
    else:
        return render(requests, 'login.html')
def web_logout(requests):
    try:
        logout(requests)
        messages.success("注销成功")
    except BaseException as e:
        logger.debug("用户退出失败，原因：%s" %e)
        messages.error("注销失败")
@login_required
def user_add(requests):
    try:
        username = requests.POST['username']
        password = requests.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(requests, '用户添加成功')
    except BaseException as e:
        logger.debug("用户添加失败，原因：%s" %e)
        messages.error(requests,'用户添加失败')
@login_required
def user_del(requests):
    try:
        username = requests.POST['username']
        User.objects.filter(username=username).delete()
        messages.success("用户删除成功")
    except BaseException as e:
        logger.debug("用户删除失败，原因：%s" %e)
        messages.error("用户删除失败")
@login_required
def user_change_passwd(requests):
    try:
        username = requests.POST['username']
        password = requests.POST['password']
        User.objects.filter(username=username).update(password=password)
        messages.success("密码修改成功")
    except BaseException as e:
        logger.debug("密码修改失败，原因：%s" %e)
        messages.error("密码修改失败")

