from functools import wraps
from importlib.resources import path

from sympy import content
from flask import Flask, request, render_template, redirect, url_for, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, null, or_,not_,func
from models import *
from manage import *
from flask_cors import CORS
import config
import datetime,time

app = Flask(__name__,
            static_folder = "../frontend/dist/static",
            template_folder = "../frontend/dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(config)
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
db = SQLAlchemy(app)


# 登录接口，判断用户名密码是否合法
@app.route('/api/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            user = get_user_byusername(request.form['username'])
            response=user_to_content(user)
            return jsonify(response)
    return sendmsg('fail')

# 获取当前登录用户的用户名
@app.route('/api/get_user/',methods=['POST'])
def get_user():
    user = get_user_byusername(request.form['username'])
    response=user_to_content(user)
    return jsonify(response)

# 根据用户id获取用户
@app.route('/api/get_user_byid/',methods=['POST'])
def get_user_byid():
    user=User.query.filter(User.id==request.form['userid']).first()
    return jsonify(user_to_content(user))

# 登出接口
@app.route('/api/logout/',methods=['GET'])
def logout():
    return sendmsg('success')

# 注册接口
# 获取用户名、密码、邮箱，向User数据库插入新的条目
@app.route('/api/regist/', methods=['POST'])
def regist():
    if request.method == 'POST':
        username = User.query.filter(User.username == request.form['username']).first()
        email = User.query.filter(User.email == request.form['email']).first()
        if(username or email):
            return sendmsg('fail')
        else:
            id=get_newid()
            newUser=User(id=id, username=request.form['username'], password=request.form['password'],
                email=request.form['email'])
            db.session.add(newUser)
            db.session.commit()
    return sendmsg('success')

# 团队创建接口
@app.route('/api/creategroup/',methods=['POST'])
def creategroup():
   user=get_user_byusername(request.form['username'])
   id=get_newid()
   newGroup=Group(id=id,groupname=request.form['groupname'],leaderid=user.id,createdtime=datetime.datetime.now(),description=request.form['description'])
   newGroupMember=GroupMember(id=id,group_id=id,user_id=user.id)
   db.session.add(newGroup)
   db.session.add(newGroupMember)
   db.session.commit()
   return sendmsg('success')

# 获取当前user加入/创建的所有团队
@app.route('/api/mygroup/',methods=['POST'])
def mygroup():
    user=get_user_byusername(request.form['username'])
    all_groupmember=GroupMember.query.filter(GroupMember.user_id==user.id).all()
    res=[]
    for groupmember in all_groupmember:
        group=Group.query.filter(Group.id==groupmember.group_id).first()
        # if(group.leaderid!=user.id):
        res.append(group_to_content(group))
    return jsonify(res)

# 判断是否是由自己创建的团队（涉及相关权限）
@app.route('/api/groupiscreatedbyme/',methods=['POST'])
def groupiscreatedbyme():
    user=get_user_byusername(request.form['username'])
    res=Group.query.filter(and_(Group.leaderid==user.id,Group.id==request.form['groupid'])).first()
    if(res):
        return sendmsg('yes')
    return sendmsg('no')

# 邀请的用户已经同意，向团队中添加新成员，并向队长发送私信
@app.route('/api/addgroupmember/',methods=['POST'])
def addgroupmember():
    userid=request.form['userid']
    user=User.query.filter(User.id==userid).first()
    groupid=request.form['groupid']
    group=Group.query.filter(Group.id==groupid).first()
    id=get_newid()
    newGroupMember=GroupMember(id=id,user_id=userid,group_id=groupid)
    db.session.add(newGroupMember)
    db.session.commit()

    id=get_newid()
    now=datetime.datetime.now()
    send_time=now.strftime('%Y-%m-%d')
    content=user.username+"通过了你的邀请，加入团队("+group.groupname+")"
    new_notice=Notice(id=id,sender_id=userid,receiver_id=group.leaderid,document_id=0,
        group_id=groupid,send_time=now,content=content,type=1
    )
    db.session.add(new_notice)
    db.session.commit()

    all_document=db.session.query(Document).filter(Document.group_id==groupid).all()
    for document in all_document:
        id=get_newid()
        newDU=DocumentUser(id=id,document_id=document.id,
            user_id=userid,last_watch=0,
            favorited=0,type=1,modified_time=0)
        db.session.add(newDU)
        db.session.commit()
    del_notice(request.form['id'])
    response={
        'message':'success'
    }
    return jsonify(response)


# 拒绝团队邀请
# 向邀请者发送拒绝信息
@app.route('/api/refuse_groupmember/',methods=['POST'])
def refuse_groupmember():
    userid=request.form['userid']
    user=User.query.filter(User.id==userid).first()
    groupid=request.form['groupid']
    group=Group.query.filter(Group.id==groupid).first()

    id=get_newid()
    now=datetime.datetime.now()
    send_time=now.strftime('%Y-%m-%d')
    content=user.username+"拒绝了你的邀请，不加入团队("+group.groupname+")"
    new_notice=Notice(id=id,sender_id=userid,receiver_id=group.leaderid,document_id=0,
        group_id=groupid,send_time=now,content=content,type=5
    )
    db.session.add(new_notice)
    del_notice(request.form['id'])
    db.session.commit()
    
    response={
        'message':'success'
    }
    return jsonify(response)

# 根据用户名搜索用户（成员邀请）
@app.route('/api/queryuser/',methods=['POST'])
def queryuser():
    keyword=request.form['keyword']
    groupid=request.form['groupid']
    res=[]
    all_user=get_user_bykeyword(keyword)
    all_group_user=get_user_ingroup(groupid)
    for user in all_user:
        check=1
        for group_user in all_group_user:
            if group_user.id==user.id:
                check=0
                continue
        if check==1:
            content={
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'description':user.description
            }
            res.append(content)
    return jsonify(res)

# 团队创建者向用户发送邀请信息
@app.route('/api/invite_user/',methods=['POST'])
def invite_user():
    group_id=request.form['group_id']
    group=Group.query.filter(Group.id==group_id).first()
    user_id=request.form['user_id']
    sender=User.query.filter(User.username==request.form['leader_username']).first()
    notice=Notice.query.filter(and_(and_(Notice.group_id==group_id,Notice.sender_id==sender.id),and_(Notice.type==2,Notice.receiver_id==user_id))).first()
    if(notice):
        response={
            'message':'success'
        }
        return jsonify(response)
    id=get_newid()
    now=datetime.datetime.now()
    send_time=now.strftime('%Y-%m-%d')
    content=sender.username+"邀请你加入团队("+group.groupname+")"
    new_notice=Notice(id=id,sender_id=sender.id,receiver_id=user_id,document_id=0,
        group_id=group_id,send_time=now,content=content,type=2
    )
    db.session.add(new_notice)
    db.session.commit()
    response={
        'message':'success'
    }
    return jsonify(response)

# 查找某团队的成员
@app.route('/api/get_user_bygroup/',methods=['POST'])
def get_user_bygroup():
    all_group_user=get_user_ingroup(request.form['groupid'])
    res=[]
    for user in all_group_user:
        content={
            'id':user.id,
            'username':user.username,
            'email':user.email
        }
        res.append(content)
    return jsonify(res)

# 团队创建者解散团队，将团队文档从各个成员的文档列表中删除
@app.route('/api/delete_group/',methods=['POST'])
def delete_group():
    groupid=request.form['groupid']
    db.session.query(GroupMember).filter(GroupMember.group_id==request.form['groupid']).delete()
    db.session.query(Group).filter(Group.id==request.form['groupid']).delete()
    db.session.commit()
    all_document=db.session.query(Document).filter(Document.group_id==groupid).all()
    for document in all_document:
        db.session.query(DocumentUser).filter(DocumentUser.document_id==document.id).delete()
        
        db.session.commit()
    db.session.query(Document).filter(Document.group_id==groupid).delete()
    db.session.commit()
    return jsonify({'message':'success'})


# 文档创建接口
@app.route('/api/create_personal_doc/', methods=['POST'])
def create_personal_doc():
    msg=''
    if request.method == 'POST':
        id = get_newid()
        user = User.query.filter(User.username==request.form['username']).first()
        creator_id=user.id
        now=datetime.datetime.now()
        content=request.form['content']
        msg="success"
        newDocument=Document(id=id,title=request.form['title'], 
            creator_id=creator_id,created_time=now,
            modify_right=request.form['modify_right'],
            share_right=request.form['share_right'],
            discuss_right=request.form['discuss_right'],
            others_modify_right=request.form['modify_right'],
            others_share_right=request.form['share_right'],
            others_discuss_right=request.form['discuss_right'],
            content=content,recycled=0,is_occupied=0,
            group_id=0,
            modified_time=now)
        db.session.add(newDocument)
        db.session.commit()
        id=get_newid()
        newDU=DocumentUser(id=id,document_id=newDocument.id,
            user_id=user.id,
            favorited=0,modified_time=now,type=0)
        db.session.add(newDU)
        db.session.commit()
    response={
        'message':msg
    }
    return jsonify(response)

# 查找我拥有的文档（包括创建和被分享、包括个人文档和加入团队拥有的文档）
@app.route('/api/my_docs/',methods=['POST'])
def my_docs():
    user=User.query.filter(User.username==request.form['username']).first()
    all_du=DocumentUser.query.filter(DocumentUser.user_id==user.id).all()
    res=[]
    for du in all_du:
        doc=Document.query.filter(du.document_id==Document.id).first()
        if doc.recycled == 0:
            res.append(document_to_content(doc))
    return jsonify(res)

# 查找我创建的文档
@app.route('/api/my_created_docs/',methods=['POST'])
def my_created_docs():
    user=User.query.filter(User.username==request.form['username']).first()
    all_document=Document.query.filter(and_(Document.creator_id==user.id,Document.recycled==0)).all()
    res=[]
    for document in all_document:
        if document.recycled == 0:
            res.append(document_to_content(document))
    return jsonify(res)

# 文档删除接口
@app.route('/api/my_deleted_docs/',methods=['POST'])
def my_deleted_docs():
    user=User.query.filter(User.username==request.form['username']).first()
    all_document=Document.query.filter(and_(Document.creator_id==user.id,Document.recycled==1)).all()
    res=[]
    for document in all_document:
        res.append(document_to_content(document))
    return jsonify(res)

# 传递权限信息
@app.route('/api/tell_doc_right/',methods=['POST'])
def tell_doc_right():
    document = Document.query.filter(Document.id == request.form['DocumentID']).first()
    user=User.query.filter(User.username==request.form['username']).first()
    DUlink=db.session.query(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).first()
    if(DUlink==None):
        response={
            'watch_right':False,
            'modify_right':False,
            'share_right':False,
            'discuss_right':False,
            'others_modify_right':False,
            'others_share_right':False,
            'others_discuss_right':False,
            'others_watch_right':False,
            'doctype':-1,
            'usertype':-1,
            'isleader':False
        }
    elif user.id==document.creator_id:
        if document.group_id!=0:
            type=0
        else:
            type=1
        response={
            'watch_right':True,
            'modify_right':True,
            'share_right':True,
            'discuss_right':True,
            'others_modify_right':True,
            'others_share_right':True,
            'others_discuss_right':True,
            'others_watch_right':True,
            'doctype':type,
            'usertype':DUlink.type,
            'isleader':True
        }
    else:
        if document.group_id!=0:
            type=0
        else:
            type=1

        modify_right=toTF(document.modify_right)
        share_right=toTF(document.share_right)
        discuss_right=toTF(document.discuss_right)
        
        others_modify_right=toTF(document.others_modify_right)
        others_share_right=toTF(document.others_share_right)
        others_discuss_right=toTF(document.others_discuss_right)
        response={
            'watch_right':True,
            'modify_right':modify_right,
            'share_right':share_right,
            'discuss_right':discuss_right,
            'others_modify_right':others_modify_right,
            'others_share_right':others_share_right,
            'others_discuss_right':others_discuss_right,
            'others_watch_right':True,
            'doctype':type,
            'usertype':DUlink.type,
            'isleader':False
        }
    return jsonify(response)     

# 告知文档当前权限
@app.route('/api/tell_current_doc_right/',methods=['POST'])
def tell_current_doc_right():
    document = Document.query.filter(Document.id == request.form['DocumentID']).first()
    response={
        'modify_right':document.modify_right,
        'share_right':document.share_right,
        'discuss_right':document.discuss_right,
        'others_modify_right':document.others_modify_right,
        'others_share_right':document.others_share_right,
        'others_discuss_right':document.others_discuss_right,
    }
    return jsonify(response)

# 获取文档
@app.route('/api/get_doccontent/', methods=['POST'])
def get_doccontent():
    msg=''
    mcontent=''
    mtime=datetime.datetime.now()
    if request.method == 'POST':
        document = Document.query.filter(Document.id == request.form['DocumentID']).first()
        user=User.query.filter(User.username==request.form['username']).first()
        if (document==None) or (user==None):
            msg="fail"
            mcontent=""
            response={
                'message':msg,
                'content':mcontent
            }
            return jsonify(response)
        DUlink=db.session.query(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).first()
        if (document!=None) and (DUlink!=None):
            msg="success"
            mcontent=document.content
            now=datetime.datetime.now()
            mtime=now
            db.session.query(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).update({"last_watch":now})
            db.session.commit()
        else:
            msg="fail"
            mcontent=""
    response={
        'message':msg,
        'content':mcontent,
        'time':mtime
    }
    return jsonify(response)


# 获取文档标题
@app.route('/api/get_doctitle/',methods=['POST'])
def get_doctitle():
    msg=''
    mtitle=''
    mtime=datetime.datetime.now()
    if request.method == 'POST':
        document = Document.query.filter(Document.id == request.form['DocumentID']).first()
        user=User.query.filter(User.username==request.form['username']).first()
        if (document==None) or (user==None):
            msg="fail"
            mcontent=""
            response={
                'message':msg,
                'title':mtitle
            }
            return jsonify(response)
        DUlink=db.session.query(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).first()
        if (document!=None) and (DUlink!=None):
            msg="success"
            mtitle=document.title
            now=datetime.datetime.now()
            mtime=now
            db.session.query(DocumentUser).filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).update({"last_watch":now})
            db.session.commit()
        else:
            msg="fail"
            mtitle=""
    response={
        'message':msg,
        'title':mtitle,
        'time':mtime
    }
    return jsonify(response)


# 获取文档类型（个人或团队）
@app.route('/api/get_doc_type/',methods=['POST'])
def get_doc_type():
    newdoc=db.session.query(GroupDocument).filter(GroupDocument.document_id==request.form['documentid']).first()
    if (newdoc):
        content={"docType":1}
    else:
        content={"docType":0}
    return jsonify(content)

# 修改文档
@app.route('/api/modify_doc/', methods=['POST'])
def modify_doc():
    msg=''
    if request.method == 'POST':
        id = get_newid()
        document = Document.query.filter(Document.id == request.form['DocumentID']).first()
        user = User.query.filter(User.username==request.form['username']).first()
        # TODO: 目前只有创建者能修改文档
        msg="success"
        now=datetime.datetime.now()
        content=request.form['content']

        newDocument=Document(id=id,title=document.title, 
            creator_id=user.id,created_time=now,
            modify_right=document.modify_right,
            share_right=document.share_right,
            discuss_right=document.discuss_right,
            others_modify_right=document.modify_right,
            others_share_right=document.share_right,
            others_discuss_right=document.discuss_right,
            content=content,recycled=0,is_occupied=0,
            group_id=0,
            modified_time=now)
        db.session.add(newDocument)
        db.session.commit()

        db.session.query(DocumentUser).filter(and_(DocumentUser.user_id==user.id,
            DocumentUser.document_id==request.form['DocumentID'])).update({"modified_time":now})
        db.session.query(DocumentUser).filter(and_(DocumentUser.user_id==user.id,
            DocumentUser.document_id==request.form['DocumentID'])).update({"document_id":id})
        db.session.commit()
    response={
        'message':msg,
        'id':id
    }
    return jsonify(response)

# 文档回溯
@app.route('/api/memory_back/',methods=['POST'])
def memory_back():
    msg=''
    if request.method == 'POST':
        #其实这里用时间查找很假，但是至少在当前场景是正确的
        user = User.query.filter(User.username==request.form['username']).first()
        document = Document.query.filter(and_(Document.modified_time == request.form['time'],Document.creator_id == user.id)).first()
        id = document.id
        msg="success"
        #更新id和更改时间即可
        db.session.query(DocumentUser).filter(and_(DocumentUser.user_id==user.id,
            DocumentUser.document_id==request.form['DocumentID'])).update({"modified_time":document.modified_time})
        db.session.query(DocumentUser).filter(and_(DocumentUser.user_id==user.id,
            DocumentUser.document_id==request.form['DocumentID'])).update({"document_id":id})
        db.session.commit()
    response={
        'message':msg,
        'id':id
    }
    return jsonify(response)


# 向用户发送信息
@app.route('/api/message_user/',methods=['POST'])
def message_user():
    msg=''
    if request.method=='POST':
        sender = User.query.filter(User.username==request.form['sender']).first()
        receiver = User.query.filter(User.username==request.form['receiver']).first()

        # 发送消息
        id=get_newid()
        now=datetime.datetime.now()
        send_time=now.strftime('%Y-%m-%d')
        content = sender.username+": "+request.form['message']
        new_notice=Notice(id=id,sender_id=sender.id,receiver_id=receiver.id,
            group_id=0,send_time=now,content=content,type=100
        )
        msg='success'
        db.session.add(new_notice)
        db.session.commit()
    response={
        'message':msg
    }
    return jsonify(response)

# 个人文档分享
@app.route('/api/pernal_doc_share_to/',methods=['POST'])
def personal_share_to():
    msg=''
    if request.method=='POST':
        document = Document.query.filter(Document.id == request.form['DocumentID']).first()
        user = User.query.filter(User.username==request.form['username']).first()
        template_doc = DocumentUser.query.filter(DocumentUser.document_id == request.form['DocumentID']).first()
        target_user=User.query.filter(User.email==request.form['Email']).first()
        id=get_newid()
        newDU=DocumentUser(id=id,document_id=document.id,
            user_id=target_user.id,last_watch=template_doc.last_watch,
            favorited=template_doc.favorited,type=0,modified_time=template_doc.modified_time)

        # 发送消息
        id=get_newid()
        now=datetime.datetime.now()
        send_time=now.strftime('%Y-%m-%d')
        content=user.username+"分享给你了一个文档("+document.title+")"
        new_notice=Notice(id=id,sender_id=user.id,receiver_id=target_user.id,document_id=document.id,
            group_id=0,send_time=now,content=content,type=4
        )
        msg='success'
        db.session.add(new_notice)
        db.session.add(newDU)
        db.session.commit()
    response={
        'message':msg
    }
    return jsonify(response)

# 添加团队共享文档
@app.route('/api/add_group_doc/', methods=['POST'])
def add_group_doc():
    doc=GroupDocument.query.filter(GroupDocument.document_id == request.form['documentid']).first()
    print(doc)
    if(doc):
        print("here")
        return sendmsg('fail')
    else:
        id=get_newid()
        id2=get_newid()
        newGroupDocument=GroupDocument(id=id, group_id=request.form['groupid'], document_id=request.form['documentid'])
        # print(newGroupDocument)
        db.session.add(newGroupDocument)
        db.session.commit()
        all_member=GroupMember.query.filter(GroupMember.group_id==request.form['groupid']).all()
        group=Group.query.filter(Group.id==request.form['groupid']).first()
        doc=db.session.query(Document).filter(Document.id==request.form['documentid']).first()
        print(all_member)
        i=0
        for member in all_member:
            # print(member.user_id, group.leaderid)
            if(member.user_id != group.leaderid):
              newDU=DocumentUser(id=id2+i, document_id=request.form['documentid'], 
              user_id=member.user_id, last_watch=doc.modified_time, is_creator=0, share_right=0, watch_right=1, modify_right=1, delete_right=0, 
              favorited=0,modified_time=doc.modified_time,type=1)  
              db.session.add(newDU)
              db.session.commit()
              i = i + 1
        return sendmsg('success')

# 获取团队共享文档
@app.route('/api/get_group_doc/', methods=['POST'])
def get_group_doc():
    groupid=request.form['groupid']
    all_document=db.session.query(GroupDocument).filter(GroupDocument.group_id==groupid).all()
    res=[]
    for doc in all_document:
        document=db.session.query(Document).filter(Document.id==doc.document_id).first()
        content={
            'id':document.id,
            'title':document.title,
            'modifiedTime':document.modified_time
        }
        res.append(content)
    return jsonify(res)


# 删除团队共享文档
@app.route('/api/delete_group_doc/', methods=['POST'])
def delete_group_doc():
    docid=request.form['documentid']
    all_member=GroupMember.query.filter(GroupMember.group_id==request.form['groupid']).all()
    group=Group.query.filter(Group.id==request.form['groupid']).first()
    doc = Document.query.filter(Document.id == docid).first()
    print(docid)
    print(doc)
    for member in all_member:
      if(member.user_id != group.leaderid):
        db.session.query(DocumentUser).filter(DocumentUser.document_id==docid and DocumentUser.user_id==member.user_id and DocumentUser.user_id!=doc.creator_id).delete()
    db.session.query(GroupDocument).filter(GroupDocument.document_id==docid).delete()
    db.session.commit()
    return sendmsg('success')

# 修改文档信息
@app.route('/api/modify_doc_basic/',methods=['POST'])
def modify_doc_basic():
    document = Document.query.filter(Document.id == request.form['DocumentID']).first()
    user = User.query.filter(User.username==request.form['username']).first()
    if(user.id == document.creator_id):
        db.session.query(Document).filter(Document.id==request.form['DocumentID']).update({"title":request.form['title']})
        db.session.commit()
        return sendmsg("success")
    return sendmsg("fail")


# 文档删除（放入回收站）
@app.route('/api/recycle_doc/', methods=['POST'])
def recycle_doc():
    msg=''
    if request.method=='POST':
        document = Document.query.filter(Document.id == request.form['DocumentID']).first()
        user = User.query.filter(User.username==request.form['username']).first()
        DUlink=DocumentUser.query.filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).first()
        # if (document!=None) and (DUlink.delete_right==1)and (document.recycled==0):
        if (document!=None) and (document.recycled==0) and (document.creator_id==user.id):
            msg='success'
            db.session.query(Document).filter(Document.id==request.form['DocumentID']).update({"recycled":1})
            db.session.commit()
        else:
            msg='fail'
    response={
        'message':msg
    }
    return jsonify(response)

# 文件从回收站中删除（彻底删除）
@app.route('/api/del_doc/', methods=['POST'])
def del_doc():
    msg=''
    if request.method=='POST':
        document = Document.query.filter(Document.id == request.form['DocumentID']).first()
        user = User.query.filter(User.username==request.form['username']).first()
        DUlink=DocumentUser.query.filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).first()
        if (document!=None) and (document.recycled==1) and (document.creator_id==user.id):
            msg='success'
            db.session.query(Document).filter(Document.id==request.form['DocumentID']).update({"recycled":2})
            db.session.commit()
        else:
            msg='fail'
    response={
        'message':msg
    }
    return jsonify(response)

# 恢复文档
@app.route('/api/recover_doc/', methods=['POST'])
def recover_doc():
    msg=''
    if request.method=='POST':
        document = Document.query.filter(Document.id == request.form['DocumentID']).first()
        user = User.query.filter(User.username==request.form['username']).first()
        DUlink=DocumentUser.query.filter(and_(DocumentUser.document_id==document.id,DocumentUser.user_id==user.id)).first()
        # if (document!=None) and (DUlink.delete_right==1)and (document.recycled==0):
        if (document!=None) and (document.recycled==1) and (document.creator_id==user.id):
            msg='success'
            db.session.query(Document).filter(Document.id==request.form['DocumentID']).update({"recycled":0})
            db.session.commit()
        else:
            msg='fail'
    response={
        'message':msg
    }
    return jsonify(response)


# 发布新评论
@app.route('/api/create_comment/', methods=['POST'])
def create_comment():
    msg=''
    if request.method == 'POST':
        id=get_newid()
        user = User.query.filter(User.username==request.form['username']).first()
        creator_id=user.id
        document_id=request.form['DocumentID']
        document=Document.query.filter(Document.id==document_id).first()
        now=datetime.datetime.now()
        content=request.form['content']
        msg="success"
        newComment=Comment(id=id,document_id=document_id,creator_id=creator_id,content=content,created_time=now)
        db.session.add(newComment)
        db.session.commit()

        # 发送消息
        id=get_newid()
        send_time=now.strftime('%Y-%m-%d')
        content=user.username+" in your doc("+document.title+")leave a comment"
        new_notice=Notice(id=id,sender_id=user.id,receiver_id=document.creator_id,document_id=document_id,
            group_id=0,send_time=now,content=content,type=3
        )
        db.session.add(new_notice)
        db.session.commit()

    response={
        'message': msg
    }
    return jsonify(response)

# 获取文档的所有评论
@app.route('/api/get_all_comment/', methods=['POST'])
def get_all_comment():
    all_comment=Comment.query.filter(Comment.document_id==request.form['DocumentID']).all()
    res=[]
    for comment in all_comment:
        user=User.query.filter(User.id==comment.creator_id).first()
        res.append(comment_to_content(comment,user))
    res.reverse()
    return jsonify(res)

# 获取文档所有修改记录
@app.route('/api/get_all_modified_time/',methods=['POST'])
def get_all_modified_time():
    res=[]
    user = db.session.query(DocumentUser).filter(DocumentUser.document_id==request.form['DocumentID']).first()
    all_modified_time=db.session.query(Document).filter(and_(Document.creator_id==user.user_id,Document.modified_time!=0)).order_by(-Document.modified_time)
    for tmp in all_modified_time:
        user=User.query.filter(User.id==tmp.creator_id).first()
        res.append(modifiedtime_to_content(tmp,user))
    document=Document.query.filter(Document.id==request.form['DocumentID']).first()
    user=User.query.filter(User.id==document.creator_id).first()
    res.append(created_info(document,user))
    return jsonify(res)

# 获取用户未读的消息
@app.route('/api/get_all_notice/',methods=['POST'])
def get_all_notice():
    receiver=User.query.filter(User.username==request.form['receiver_username']).first()
    all_notice=Notice.query.filter(Notice.receiver_id==receiver.id).all()
    res=[]
    for notice in all_notice:
        res.append(notice_to_content(notice))
    return jsonify(res)

# 删除未读消息
@app.route('/api/del_new_notice/',methods=['POST'])
def del_new_notice():
    new_notice_id=request.form['new_notice_id']
    del_notice(new_notice_id)
    response={
        'message':'success'
    }
    return jsonify(response)

# 私信接口
@app.route('/api/view_message/',methods=['POST'])
def view_message():
    receiver=User.query.filter(User.username==request.form['receiver_username']).first()
    all_notice=Notice.query.filter(Notice.receiver_id==receiver.id).all()
    res=[]
    for notice in all_notice:
        stat=notice.type
        if(stat==100):
            res.append(notice_to_content(notice))
    return jsonify(res)

# 查看邀请信息
@app.route('/api/view_confirm_notice/',methods=['POST'])
def view_confirm_notice():
    receiver=User.query.filter(User.username==request.form['receiver_username']).first()
    all_notice=Notice.query.filter(and_(Notice.receiver_id==receiver.id,Notice.type==2)).all()
    res=[]
    for notice in all_notice:
        res.append(notice_to_content(notice))
    print(res)
    return jsonify(res)


@app.route('/api/sayhi/',methods=['POST'])
def sayhi():
    receiver=User.query.filter(User.username==request.form['receiver_username']).first()
    sender=User.query.filter(User.username==request.form['sender_username']).first()
    id=get_newid()
    now=datetime.datetime.now()
    new_msg=Message(id=id,sender_id=sender.id,receiver_id=receiver.id,send_time=now,content='hi')
    db.session.add(new_msg)
    db.session.commit()
    response={
        'message':'success'
    }
    return jsonify(response)

# 向某人发送消息
@app.route('/api/send_msg_to_sb/',methods=['POST'])
def send_msg_to_sb():
    receiver=User.query.filter(User.username==request.form['receiver_username']).first()
    sender=User.query.filter(User.username==request.form['sender_username']).first()
    id=get_newid()
    now=datetime.datetime.now()
    content=request.form['content']
    new_msg=Message(id=id,sender_id=sender.id,receiver_id=receiver.id,send_time=now,content=content)
    db.session.add(new_msg)
    db.session.commit()
    response={
        'id':id,
        'receiver_name':receiver.username,
        'sender_name':sender.username,
        'send_time':now,
        'content':content
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='192.168.1.111',port = 5000)