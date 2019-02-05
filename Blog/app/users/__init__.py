#与用户相关的操作
#如：用户的注册，登录，登出，...
from flask import Blueprint
user_blueprint = Blueprint('users',__name__)
from . import views