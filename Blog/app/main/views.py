#处理main业务中的路由和视图处理函数
import json
import os

from sqlalchemy import func

from . import main_blueprint as main
from .. import db
from ..models import *
from flask import render_template, request, session, redirect
import datetime



#首页
@main.route('/')
def main_index():
    #查询Category中所有的数据
    categories = Category.query.all()
    #查询Ｔopic中所有的数据
    topics = Topic.query.all()
    #查询Topic中的阅读量按照从大到小排序
    topicss = Topic.query.order_by("read_num desc,id desc").all()
    # 用冒泡排序的方法查询出点赞数量并按照从大到小排序
    topic_like = topics
    for i in range(len(topic_like)-1):    # 这个循环负责设置冒泡排序进行的次数
        for j in range(len(topic_like)-i-1):  # ｊ为列表下标
            if topic_like[j].voke_users.count() < topic_like[j+1].voke_users.count():
                topic_like[j], topic_like[j+1] = topic_like[j+1], topic_like[j]

    #从session中获取登录信息(id,loginname)
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(id=id).first()
    return render_template('index.html',params=locals())

#登录
@main.route('/login',methods=['GET','POST'])
def login_views():
    if request.method == 'GET':
        #判断id和loginname是否在session中
        if 'id' in session and 'loginname' in session:
            return redirect('/')
        #记录请求的源地址,并将请求源地址保存进session
        url = request.headers.get('Referer','/')
        session['url'] = url
        return render_template('login.html',params=locals())
    else:
        #接收传递过来的用户名或密码
        loginname = request.form.get('username')
        upwd = request.form.get('password')
        #验证用户名和密码是否正确
        user=User.query.filter_by(loginname=loginname,upwd=upwd).first()
        #如果登录成功,存进session,则返回到请求的源地址
        if user:
            session['id'] = user.id
            session['loginname'] = user.loginname
            url = session['url']
            return redirect(url)
        else:
            #如果失败,则返回到登录页面
            return render_template('login.html')
#退出
@main.route('/logout')
def logout_views():
    #获取请求源地址,如果没有则将'/'作为请求源地址
    url=request.headers.get('Referer','/')
    #判断session中是否有登录信息,如果有则清除
    if 'id' in session and 'loginname' in session:
        del session['id']
        del session['loginname']
    #重定向到请求源地址上
        return redirect(url)

#注册
@main.route('/register',methods=['GET','POST'])
def register_views():
    if request.method == 'GET':
        url = request.headers.get('Referer', '/')
        session['url'] = url
        return render_template('register.html')
    else:
        loginname=request.form.get('loginname')
        username = request.form.get('username')
        email = request.form.get('email')
        url = request.form.get('url')
        password = request.form.get('password')
        user = User()
        user.uname = username
        user.loginname = loginname
        user.email = email
        user.url = url
        user.upwd = password
        db.session.add(user)
        user = User.query.filter_by(loginname=loginname, upwd=password).first()
        session['id'] = user.id
        session['loginname'] = user.loginname
        url = session['url']
        return redirect(url)

# #注册验证
@main.route('/verify',methods=['GET','POST'])
def verify_views():
    if request.method == 'GET':
        # GETＦ方式获取前端Ajax昵称
        username = request.args.get('username')
        # 查询
        uname = User.query.filter_by(uname=username).first()
        if uname:
            dic = {
                'status':0,
                'msg':'用户存在'
            }
            return json.dumps(dic)
        elif username == '':
            dic = {
                'status': 1,
                'msg': '空'
            }
            return json.dumps(dic)
        else:
            dic = {
                'status': 2,
                'msg': '可以使用'
            }
            return json.dumps(dic)
    else:
        # 获取前端Ajax用户名
        loginname1 = request.form.get('loginname')
        # 查询
        loginname = User.query.filter_by(loginname=loginname1).first()
        if loginname:
            dic = {
                'status': 0,
                'msg': '用户存在'
            }
            return json.dumps(dic)
        elif loginname1=='':
            dic = {
                'status': 1,
                'msg': '空'
            }
            return json.dumps(dic)
        else:
            dic = {
                'status': 2,
                'msg': '可以使用'
            }
            return json.dumps(dic)




#发表博客
@main.route('/release',methods=['GET','POST'])
def release_views():
    if request.method == 'GET':
        #判断是否有登录用户
        if 'id' in session and 'loginname' in session:
            #有登录用户,则取出信息判断is_author
            user=User.query.filter_by(id=session['id']).first()
            #判断is_author
            if user.is_author:
                #读取category所有信息
                categories = Category.query.all()
                # 查询Topic中的阅读量按照从大到小排序
                topicss = Topic.query.order_by("read_num desc,id desc").all()
                return render_template('release.html',params=locals())
            else:
                return render_template('Prompt.html')
        else:
            return redirect('/login')
    else:
        #post请求处理发表博客的相关操作
        #1.创建Topic的对象 - topic
        topic = Topic()
        #2.接收前端传递过来的值并赋值给topic
        #2.1 接收传递过来的标题title - author
        topic.title=request.form['author']
        #2.2 接收传递过来的blogtype_id - list
        topic.blogtype_id=request.form['list']
        #2.3 接收传递过来的category_id -category
        topic.category_id=request.form['category']
        #2.4 从session中得到用户的user_id - session['id']
        topic.user_id=session['id']
        #2.5 接收传递过来的content - content
        topic.content=request.form['content']
        #2.6 获取系统时间(年月日时分秒)给pub_date
        topic.pub_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #3. 判断是否有文件上传,如果有的话则将保存至static/upload,并将路径给images
        if request.files:
            print('zcasdadas')
            #获取要上传的文件
            f=request.files['picture']
            #处理文件名:时间.扩展名
            ftime=datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            ext=f.filename.split('.')[1]
            filename=ftime+'.'+ext
            #处理上传路径: static/upload
            topic.images='upload/'+filename
            #将文件以文件名的形式保存到指定路径下(绝对路径)
            basedir=os.path.dirname(os.path.dirname(__file__))
            upload_path=os.path.join(basedir,'static/upload',filename)
            f.save(upload_path)
        #4. 将topic保存回数据库
        db.session.add(topic)
        return render_template('Prompt_win.html')

#详细博客
@main.route('/info',methods=['GET','POST'])
def info_views():
    if request.method == 'GET':
        # 从session中获取登录信息(id,loginname)
        if 'id' in session and 'loginname' in session:
            id = session['id']
            user = User.query.filter_by(id=id).first()
        else:
            user = ''
        #1.接收传递过来的id参数值(即向查看的博客的id)
        topic_id = request.args['id']
        #2.根据id查询出对应的博客
        topic = Topic.query.filter_by(id=topic_id).first()
        #3.更新阅读量(将原有的read_num+1再存进取)
        topic.read_num = int(topic.read_num) + 1
        db.session.add(topic)
        #及时提交
        db.session.commit()
        #4.查询上一篇(查询出id比当前topic_id小的博客中的最后一篇博客,如果结果为None则表示没有上一篇了)
        prevTop=db.session.query(Topic).filter(Topic.id<topic_id).order_by('id desc').first()
        #5.查询下一篇(查询出id比当前topic_id大的博客中的第一篇博客,如果结果为None则表示没有下一篇了)
        nextTop=db.session.query(Topic).filter(Topic.id>topic_id).first()
        # 查询Category中所有的数据
        categories = Category.query.all()
        # 查询Ｔopic中所有的数据
        topics = Topic.query.all()
        # 查询Topic中的阅读量按照从大到小排序
        topicss = Topic.query.order_by("read_num desc,id desc").all()
        # 用冒泡排序的方法查询出点赞数量并按照从大到小排序
        topic_like = topics
        for i in range(len(topic_like) - 1):  # 这个循环负责设置冒泡排序进行的次数
            for j in range(len(topic_like) - i - 1):  # ｊ为列表下标
                if topic_like[j].voke_users.count() < topic_like[j + 1].voke_users.count():
                    topic_like[j], topic_like[j + 1] = topic_like[j + 1], topic_like[j]
        return render_template('info.html',params=locals())
    else:
        if 'id' in session and 'loginname' in session:
            url = request.headers.get('Referer', '/')
            #创建Reply对象
            reply = Reply()
            # 接受传递过来的回复内容
            reply.content = request.form['content']
            #接受文章id
            reply.topic_id = request.form['tid']
            # 从session中得到用户的user_id - session['id']
            reply.user_id = session['id']
            #回复时间
            reply.reply_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.add(reply)
            return redirect(url)
        else:
            return redirect('/login')


#文章列表
@main.route('/list')
def list_views():
    # 从session中获取登录信息(id,loginname)
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(id=id).first()
    #查询Category中所有的数据
    categories = Category.query.all()
    #查询Ｔopic中所有的数据
    topics = Topic.query.all()
    #查询Topic中的阅读量按照从大到小排序
    topicss = Topic.query.order_by("read_num desc,id desc").all()
    # 用冒泡排序的方法查询出点赞数量并按照从大到小排序
    topic_like = topics
    for i in range(len(topic_like)-1):    # 这个循环负责设置冒泡排序进行的次数
        for j in range(len(topic_like)-i-1):  # ｊ为列表下标
            if topic_like[j].voke_users.count() < topic_like[j+1].voke_users.count():
                topic_like[j], topic_like[j+1] = topic_like[j+1], topic_like[j]
    #获取文章类型id
    ids = request.args.get('id')
    if ids:
        topics=Topic.query.filter_by(category_id=ids).all()
        return render_template('list.html', params=locals())
    else:
        return render_template('list.html',params=locals())

#我的相册
@main.route('/photo')
def photo_views():
    # 查询Ｔopic中所有的数据
    topics = Topic.query.all()
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(id=id).first()
    return render_template('photo.html',params=locals())

#时间轴
@main.route('/time')
def time_views():
    # 查询Ｔopic中所有的数据
    topics = Topic.query.all()
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(id=id).first()
    return render_template('time.html',params=locals())

#留言板块
@main.route('/gbook',methods=['GET','POST'])
def gbook_views():
    if request.method == 'GET':
        topics = Topic.query.all()
        topic_like = topics
        for i in range(len(topic_like) - 1):  # 这个循环负责设置冒泡排序进行的次数
            for j in range(len(topic_like) - i - 1):  # ｊ为列表下标
                if topic_like[j].voke_users.count() < topic_like[j + 1].voke_users.count():
                    topic_like[j], topic_like[j + 1] = topic_like[j + 1], topic_like[j]
        replys = Reply.query.all()
        if 'id' in session and 'loginname' in session:
            id = session['id']
            user = User.query.filter_by(id=id).first()
        return render_template('gbook.html',params=locals())
    else:
        if 'id' in session and 'loginname' in session:
            url = request.headers.get('Referer', '/')
            #创建Reply对象
            reply = Reply()
            # 接受传递过来的回复内容
            reply.content = request.form['content']
            # 从session中得到用户的user_id - session['id']
            reply.user_id = session['id']
            #回复时间
            reply.reply_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.add(reply)
            return redirect(url)
        else:
            return redirect('/login')

#关于我
@main.route('/about')
def about_views():
    if 'id' in session and 'loginname' in session:
        id = session['id']
        user = User.query.filter_by(id=id).first()
    return render_template('about.html',params=locals())