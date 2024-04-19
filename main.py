from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
from account import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ased5wwjkowl1j3k#'
socketio = SocketIO(app)

# Constant variables
event_join = "join"
event_leave = "leave"
event_msg_from_srv = "message_from_srv"
event_msg_to_srv = "message_to_srv"
room = "msg"


@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login')
def load_login():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # Auto login
    if checkIpAddr(ipaddr):
        session['user'] = checkIpAddr(ipaddr)[0]
        session['password'] = checkIpAddr(ipaddr)[1]
        return redirect(url_for('chat'))
    session.clear()
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    session['user'] = request.form.get('user')
    session['password'] = request.form.get('password')

    # Checking user and password
    if checkLogin(session['user'], session['password']):
        if readData(session['user'], 'ipaddr') != ipaddr:
            changeData(session['user'], 'ipaddr', ipaddr)
        activateLogin(session['user'])
        return redirect(url_for('chat'))
    else:
        session.clear()
        return render_template("login.html", blad1="Username or password is invalid.")


@app.route('/register')
def load_register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register():
    ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # Creating an account when the user doesn't have another one
    if doesExist(ipaddr):
        return render_template('register.html', blad2="You already have an account.")
    else:
        print(f"{ipaddr} : {doesExist(ipaddr)}")
        session['user'] = request.form.get('user')
        session['password'] = request.form.get('password')
        session['ipaddr'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        # Creating an account
        createAccount(request.form.get('fname'), request.form.get('lname'), session['user'], session['password'],
                      session['ipaddr'])
        return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    # The server will redirect the user when he is not logged in
    if session:
        if isLogged(session['user']):
            return render_template("chat.html", chat_history=readChatHistory())
    return redirect(url_for('login'))


# ============= SOCKETIO =============
@socketio.on(event_join, namespace='/chat')
def join(message):
    user = session['user']
    join_room(room)

    print(f"{user} has entered and joined the room.")
    emit(event_msg_from_srv, {'message': f'{user} has entered and joined the room.', 'from': "SERVER"}, room=room)


@socketio.on(event_leave, namespace='/chat')
def leave(message):
    user = session['user']
    leave_room(room)
    logout(user)

    print(f"{user} has left the room.")
    emit(event_msg_from_srv, {'message': f'{user} has left the room.', 'from': "SERVER"}, room=room)
    session.clear()

@socketio.on(event_msg_to_srv, namespace='/chat')
def message(message):
    user = session['user']
    msg = message['message']

    # Saving messages to chat history
    if msg.strip() != "":
        print(f"{user}: {msg}")
        saveMessage(user, msg)
        emit(event_msg_from_srv, {'message': f'{msg}', 'from': user}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

