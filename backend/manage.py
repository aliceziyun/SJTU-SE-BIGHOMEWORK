from functools import wraps
from flask import Flask, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_
from models import *
import time
import config

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
db = SQLAlchemy(app)

#calculate a new id and cal time
def get_newid():
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    id = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))
    return id

#verify input
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user: return True
    else:return False

def get_user_byusername(username):
    user = User.query.filter(User.username == username).first()
    return user

def get_user_bykeyword(keyword):
    all_user = User.query.filter(User.username.like(
        '%{keyword}%'.format(keyword=keyword))).all()
    return all_user

def get_user_ingroup(groupid):
    all_GroupMembers = GroupMember.query.filter(GroupMember.group_id == groupid).all()
    all_user = []
    for groupmember in all_GroupMembers:
        user = User.query.filter(User.id == groupmember.user_id).all()
        all_user += user
    return all_user

def get_user_indocument(documentid):
    all_documents=DocumentUser.query.filter(DocumentUser.document_id==documentid).all()
    all_user=[]
    for document in all_documents:
        user=User.query.filter(User.id==document.user_id).all()
        all_user+=user
    return all_user

def user_to_content(user):
    content = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'description': user.description
    }
    return content


def group_to_content(group):
    context = {
        'groupid': group.id,
        'groupname': group.groupname,
        'createdtime': group.createdtime,
        'description': group.description
    }
    return context


def comment_to_content(comment,user):
    content = {
        'id': comment.id,
        'document_id': comment.document_id,
        'username': user.username,
        'content': comment.content,
        'datetime': comment.time
    }
    return content


def document_to_content(document):
    content = {
        'id': document.id,
        'title': document.title,
        'creator_id': document.creator_id,
        'created_time': document.created_time,
        'modified_time': document.modified_time,
        'recycled': document.recycled,
        'is_occupied': document.is_occupied,
        'group_id': document.group_id,
    }
    return content


def notice_to_content(notice):
    type=notice.type
    sender=User.query.filter(User.id==notice.sender_id).first()
    receiver=User.query.filter(User.id==notice.receiver_id).first()
    content={}
    #doc
    if(type==3 or type==4):
        document=Document.query.filter(Document.id==notice.document_id).first()
        content = {
            'id': notice.id,
            'sender_id': notice.sender_id,
            'sender_name':sender.username,
            'receiver_id': notice.receiver_id,
            'receiver_name':receiver.username,
            'group_id': "",
            'group_name':"",
            'document_id': notice.document_id,
            'document_title':document.title,
            'datetime': notice.send_time,
            'content': notice.content,
            'type': notice.type
        }
    #message
    elif(type==100):
        content = {
            'id': notice.id,
            'sender_id': notice.sender_id,
            'sender_name':sender.username,
            'receiver_id': notice.receiver_id,
            'receiver_name':receiver.username,
            'group_id': "",
            'group_name':"",
            'document_id': notice.document_id,
            'datetime': notice.send_time,
            'content': notice.content,
            'type': notice.type
        }
    #group
    else:
        group=Group.query.filter(Group.id==notice.group_id).first()
        content = {
            'id': notice.id,
            'sender_id': notice.sender_id,
            'sender_name':sender.username,
            'receiver_id': notice.receiver_id,
            'receiver_name':receiver.username,
            'group_id': notice.group_id,
            'group_name':group.groupname,
            'document_id': "",
            'document_title':"",
            'datetime': notice.send_time,
            'content': notice.content,
            'type': notice.type
        }
    return content

def modifiedtime_to_content(document,user):
    content = {
        'document_id': document.id,
        'username':user.username,
        'datetime':document.modified_time,
        'content':'modify doc'
    }
    return content

def sendmsg(str):
    context = {
        'message': str
    }
    return jsonify(context)

def toTF(num):
    if (num):
       return True
    return False

def created_info(document,user):
    content = {
        'document_id':document.id,
        'username':user.username,
        'datetime':document.created_time,
        'content':'create doc'
    }
    return content

def del_notice(id):
    db.session.query(Notice).filter(Notice.id==id).delete()
    db.session.commit()

def msg_to_content(sender,receiver,msg):
    content={
        'id':msg.id,
        'sender_name':sender.username,
        'receiver_name':receiver.username,
        'send_time':msg.send_time,
        'content':msg.content
    }
    return content
