# _*_coding:utf-8_*_

# import os, logging, time, json, copy
import re

from django.contrib.auth.hashers import make_password
from django.db.models import Q
import jwt
from rest_framework import response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from config.config import Config
from xj_role.services.group_service import GroupService
from xj_role.services.role_service import RoleService
from ..models import *
from ..services.user_service import UserService
from ..utils.model_handle import parse_data


# 管理员添加用户
class UserAdd(APIView):
    permission_classes = (AllowAny,)
    model = BaseInfo
    params = None

    def post(self, request, *args, **kwargs):
        self.params = parse_data(request)
        # 权限验证
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            raise MyApiError(error_text, 6010)
        # 添加逻辑
        try:
            account = str(self.params.get('account', ''))
            password = str(self.params.get('password', ''))
            # platform = str(self.params.get('platform', ''))
            full_name = str(self.params.get('full_name', ''))
            nickname = str(self.params.get('nickname', ''))

            # 用户角色部门绑定
            user_role_id = self.params.get('user_role_id', None)
            user_group_id = self.params.get('user_group_id', None)

            # 边界检查
            if not account:
                raise MyApiError("account必填", 2001)

            if not password:
                raise MyApiError("password必填", 2003)

            if not full_name:
                raise MyApiError("full_name必填", 2008)

            # 账号类型判断
            if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
                account_type = 'phone'
            elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
                account_type = 'email'
            elif re.match(r'^[A-z\u4E00-\u9FA5]+\w*$', account):
                account_type = 'username'
            else:
                raise MyApiError("账号必须是用户名、手机或者邮箱，用户名不能是数字开头", 2009)

            # 检查账号是否存在
            user_list = None
            if account_type == 'phone':
                user_list = BaseInfo.objects.filter(Q(phone=account))
            elif account_type == 'email':
                user_list = BaseInfo.objects.filter(Q(email=account))
            elif account_type == 'username':
                user_list = BaseInfo.objects.filter(Q(user_name=account))

            if user_list.count() and account_type == 'phone':
                raise MyApiError("手机已被注册: " + account)
            elif user_list.count() and account_type == 'email':
                raise MyApiError("邮箱已被注册: " + account)
            elif user_list.count() and account_type == 'username':
                raise MyApiError("用户名已被注册: " + account)

            # # 检查平台是否存在
            # platform_id = None
            # platform_set = Platform.objects.filter(platform_name__iexact=platform)
            # if not platform_set.count() == 0:
            #     platform_id = platform_set.first().platform_id

            base_info = {
                'user_name': account if account_type == 'username' else '',
                'full_name': full_name,
                "nickname": nickname,
                'phone': account if account_type == 'phone' else '',
                'email': account if account_type == 'email' else '',
            }
            current_user = BaseInfo.objects.create(**base_info)
            token = jwt.encode({'account': account}, Config.getIns().get('xj_user', "JWT_SECRET_KEY", "@xzm2021!"))
            auth = {
                'user_id': current_user.id,
                'password': make_password(password, None, 'pbkdf2_sha1'),
                'plaintext': password,
                'token': token,
            }
            Auth.objects.create(**auth)
            # 用户绑定权限和部门
            if user_group_id:
                GroupService.user_bind_group(current_user.id, user_group_id)

            if user_role_id:
                RoleService.user_bind_role(current_user.id, user_role_id)

            res = {
                'err': 0,
                'msg': '注册成功',
                'data': {"user_id": current_user.id},
            }

        except SyntaxError:
            res = {
                'err': 4001,
                'msg': '语法错误'
            }
        except LookupError:
            res = {
                'err': 4002,
                'msg': '无效数据查询'
            }
        except Exception as valueError:
            res = {
                'err': valueError.err if hasattr(valueError, 'err') else 4000,
                'msg': valueError.msg if hasattr(valueError, 'msg') else valueError.args,
            }
        except:
            res = {
                'err': 4999,
                'msg': '未知错误'
            }

        return response.Response(data=res, status=None, template_name=None, headers={"Authorization": token}, content_type=None)


class MyApiError(Exception):
    def __init__(self, message, err_code=4010):
        self.msg = message
        self.err = err_code

    def __str__(self):
        # repr()将对象转化为供解释器读取的形式。可省略
        return repr(self.msg)
