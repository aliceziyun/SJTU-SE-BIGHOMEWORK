from flask import Flask, request
import json
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket

app = Flask(__name__)

users = set()
@app.route('/conn')
def index():
    print("in")
    wsock = request.environ.get('wsgi.websocket')
    print(wsock)
    users.add(wsock)
    while True:
        message = wsock.receive()
        if message:
            obj=json.loads(message)
            username=obj['username']
            print(username)
            content=obj['content']
            print(content)
            res="{\"username\":\""+username+"\",\"content\":\""+content+"\"}"
            for user in list(users):
                if user!=wsock:
                    try:
                        # print(res)
                        user.send(res)
                    except:
                        print("disconnect") 
                        users.remove(wsock)


@app.route('/test')
def hello():
    print("hello")
    return "hello"

if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0",8888),app,handler_class=WebSocketHandler)
    http_serv.serve_forever()

