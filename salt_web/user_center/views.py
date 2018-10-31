# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from user_center import models as token_db
import logging
import random
import time
logger = logging.getLogger(__name__)
# Create your views here.
def web_login(requests):
    if requests.method == "POST":
        username = requests.POST['username']
        password = requests.POST['password']
        token = requests.POST['token']
        if len(token_db.Token.objects.filter(username=username)) == 0:
            messages.error(requests, '该用户未申请验证码')
            logger.debug("用户：%s, 未申请验证码" % username)
            return render(requests, 'login.html')
        if token_db.Token.objects.filter(username=username)[0].token != token:
            messages.error(requests, '验证码错误')
            logger.debug("用户：%s, 验证码错误" % username)
            return render(requests, 'login.html')
        token_dead = time.time() - token_db.Token.objects.filter(username=username)[0].token_time
        if token_dead >= 300:
            messages.error(requests, '验证码过期')
            logger.debug("用户：%s, 验证码过期" % username)
            return render(requests, 'login.html')
        user = authenticate(username=username, password=password)
        if user:
            login(requests, user)
            logger.debug("用户：%s, 登陆成功" %username)
            return HttpResponseRedirect('/index/')
        else:
            messages.error(requests, '用户名或密码错误')
            logger.debug("用户：%s, 用户名或密码错误" %username)
            return render(requests, 'login.html')
    else:
        return render(requests, 'login.html')
@login_required
def index(requests):
    username = requests.user.username
    return_data = {'username': username}
    #需添加查询saltstack任务信息接口
    return render(requests, 'index.html', return_data)

@csrf_exempt
def add_token(requests):
    if requests.method == "POST":
        username = requests.POST['username']
        password = requests.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            token = str(random.random()).split('.')[1][:6]
            token_db.Token.objects.filter(username=username).delete()
            token_info = token_db.Token()
            token_info.username = username
            token_info.token = token
            token_info.token_time = int(time.time())
            token_info.save()
            logger.debug("用户：%s, 创建token成功" % username)
            return HttpResponse(token)
        else:
            logger.debug("用户：%s, 获取token验证失败,用户名或密码错误" %username)
            return HttpResponse("error")
    else:
        logger.debug("错误的请求token方式")
        return HttpResponse("error")

@login_required
def web_logout(requests):
    try:
        logout(requests)

    except BaseException as e:
        logger.debug("用户注销失败，原因：%s" %e)
    finally:
        return HttpResponseRedirect('/login/')

@login_required
def user_center(requests):
    #需要添加查询用户信息
    username = requests.user.username
    user_info = User.objects.get(username=username)
    return_data = {'username': username, 'email': user_info.email, 'phone': user_info.first_name}
    return render(requests, 'usercenter.html', return_data)
@login_required
def user_add(requests):
    try:
        username = requests.POST['username']
        password = requests.POST['password']
        email = requests.POST['email']
        phone = requests.POST['phone']
        user = User.objects.create_user(username=username, password=password, email=email, first_name=phone)
        user.save()
        logger.debug("用户：%s, 添加成功" % username)
        messages.success(requests, '用户添加成功', extra_tags='bg-success')
        return render(requests, 'user_manage.html')
    except BaseException as e:
        logger.debug("用户添加失败，原因：%s" %e)
        messages.error(requests,'用户添加失败', extra_tags='bg-danger')
        return render(requests, 'user_manage.html')
@login_required
def user_del(requests):
    try:
        username = requests.POST['username']
        User.objects.filter(username=username).delete()
        logger.debug("用户：%s, 删除成功" %username)
        messages.success(requests, "用户删除成功", extra_tags='bg-success')
        return render(requests, 'user_manage.html')
    except BaseException as e:
        logger.debug("用户删除失败，原因：%s" %e)
        messages.error(requests, "用户删除失败", extra_tags='bg-danger')
        return render(requests, 'user_manage.html')
@login_required
def user_change_passwd(requests):
    try:
        username = requests.user.username
        old_password = requests.POST['old_password'].strip()
        new_password = requests.POST['new_password'].strip()
        email = requests.POST['email'].strip()
        phone = requests.POST['phone'].strip()
        repeat_new_password = requests.POST['repeat_new_password']
        if new_password == repeat_new_password:
            user = authenticate(username=username, password=old_password)
            if user:
                user.set_password(new_password)
                user.save()
                User.objects.filter(username=username).update(email=email, first_name=phone)
                logger.debug("用户：%s， 密码修改成功" %username)
                messages.success(requests, "密码修改成功", extra_tags='bg-success')
                return render(requests, 'usercenter.html')
            else:
                logger.debug("用户：%s， 密码修改失败，旧密码错误" % username)
                messages.success(requests, "密码修改失败，旧密码错误", extra_tags='bg-danger')
                return render(requests, 'usercenter.html')
        else:
            logger.debug("用户：%s， 密码修改失败" % username)
            messages.success(requests, "两次输入密码不匹配，请重新输入", extra_tags='bg-danger')
            return render(requests, 'usercenter.html')
    except BaseException as e:
        logger.debug("密码修改失败，原因：%s" %e)
        messages.error(requests, "密码修改失败", extra_tags='bg-danger')
        return render(requests, 'usercenter.html')
