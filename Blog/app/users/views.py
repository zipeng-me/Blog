#与users业务相关的路由和视图处理函数
from flask import request, render_template, redirect

from . import user_blueprint as user
from .. import db
from ..models import *

@user.route('/user')
def user_index():
    return '这是users中的首页'


#点赞
@user.route('/praise')
def praise_views():
    # 获取get方式传过来的文章id
    topid=request.args.get('Topid')
    # 获取用户is
    userid=request.args.get('Userid')
    if userid:
        user=User.query.filter_by(id=userid).first()
        topic=Topic.query.filter_by(id=topid).first()
        #关联插入多对多第三张关联表
        user.voke_topics.append(topic)
        db.session.add(user)
        return render_template('Prompt_win.html')
    else:
        return redirect('/login')