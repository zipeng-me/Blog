#根据数据库编写所有的实体类
#导入　db 到models.py
from . import db
#通过db创建实体类
#创建Category类 - category表
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    cate_name = db.Column(db.String(50),nullable=False)
    #增加关联关系以及反向引用属性-针对Topic
    topics = db.relationship('Topic',backref='category',lazy='dynamic')

#创建BlogType类-blogtype表
class BlogType(db.Model):
    __tablename__ = 'blogtype'
    id = db.Column(db.Integer,primary_key=True)
    type_name = db.Column(db.String(20),nullable=False)
    #增加关联关系以及反向引用关系属性-针对Topic
    topics = db.relationship('Topic',backref='blogtype',lazy='dynamic')

#创建User类-user表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    loginname = db.Column(db.String(50),nullable=False)
    uname = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    url = db.Column(db.String(200))
    upwd = db.Column(db.String(30),nullable=False)
    is_author = db.Column(db.Boolean,default=False)
    #关联属性......  -针对　Topic
    topics = db.relationship('Topic',backref='user',lazy='dynamic')
    #增加关联关系以及反向引用关系属性-针对Reply
    replies = db.relationship('Reply',backref='user',lazy='dynamic')
    #增加关联关系以及反向引用关系属性-与Topic之间的多对多
    voke_topics = db.relationship(
        'Topic',
        secondary='voke',
        lazy='dynamic',
        backref=db.backref('voke_users',lazy='dynamic')
    )

#创建Topic类-topic
class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False)
    read_num = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text)
    #关系:一（BlogType）对多（Topic）关系
    blogtype_id = db.Column(db.Integer,db.ForeignKey('blogtype.id'))
    #关系:一（Category）对多（Topic）关系
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    #关系:一（User）对多（Topic）关系
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # 增加关联关系以及反向引用关系属性-针对Reply
    replies = db.relationship('Reply',backref='topic',lazy='dynamic')


#创建Reply类 - reply
class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    reply_time = db.Column(db.DateTime)
    #一(User)对多(Reply)关系
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #一(Topic)对多(Reply)关系
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))

#创建Voke类 -voke
class Voke(db.Model):
    __tablename__ = 'voke'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))

#创建打赏Money类　- money
class Money(db.Model):
    __tablename__ = 'money'
    id = db.Column(db.Integer,primary_key=True)
    images = db.Column(db.Text)
