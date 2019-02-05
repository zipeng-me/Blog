#main:处理与博客相关的业务逻辑们
#如：发表博客，查看博客，删除博客，...
#导入蓝图
from flask import Blueprint
#将自己加入到Bluepront中
main_blueprint = Blueprint('main',__name__)
from . import views