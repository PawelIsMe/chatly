const event_join = "join";
const event_leave = "leave";
const event_msg_from_srv = "message_from_srv";
const event_msg_to_srv = "message_to_srv";
let socketio;


/**
 * OnLoad */
window.onload = function () {
  //console.log("Connecting...");
  welcomeWindow();
  setTimeout(welcomeWindow, 2000);
  socketio = connect();
  socketio.on('connect', function() {
    //console.log("Connected!");
    join();
  });

  socketio.on('disconnect', function() {
    //leave();
  });

  /** OnMessage */
  socketio.on(event_msg_from_srv, function (message) {
    let my_user = whoami();
    let msg = message['message'];
    let from_username = message['from'];


    if (from_username === "SERVER") {

    } else if (from_username === my_user) {
      sendDivMessage(from_username, msg, "message");
    } else {
      sendDivMessage(from_username, msg, "message");
    }

  });
}

/**
 * Whoami */
function whoami() {
  return document.getElementById("my_user").innerText;
}

/**
 * Connect to server */
function connect() {
  return io.connect('http://' + document.domain + ':' + location.port + '/chat');
}

/**
 * Join server */
function join() {
  //console.log("Joining.");
  socketio.emit(event_join, {});
}

/**
 * Leave server */
function leave() {
   //console.log("Leaving.");
   socketio.emit(event_leave, {}, function () {
        socketio.disconnect();
   });
   window.location.reload();
}


/**
 * Send message */
function onSendEnter(element) {
  if (event.keyCode == 13) {
    sendMessageToSv(element.value);
    element.value = "";
  }
}

function sendMessageToSv(msg) {
  socketio.emit(event_msg_to_srv, { 'message': msg });
}

var x = "";
function sendDivMessage(user, msg, style) {
  let chat_area = document.getElementById("conversation");
  let p = document.createElement('p');
  let div = document.createElement('div');
  p.innerText = user;
  div.innerText = msg;

  p.classList.add("nick");
  div.classList.add("message");

  if (x == user) {
    chat_area.appendChild(div);
  } else {
    chat_area.appendChild(p);
    chat_area.appendChild(div);
  }
  document.getElementById('conversation').scrollTop = div.offsetHeight + div.offsetTop;
  x = user;
}

// Welcome window
function welcomeWindow() {
  var blur = document.getElementById('blur');
  var popup = document.getElementById('popup');

  blur.classList.toggle('active');
  popup.classList.toggle('active');
}