const messageList = document.getElementById("message-list");
const messageInput = document.getElementById("message-input");
let websocket;

function sendMessage() {
    websocket.send(JSON.stringify({
        action: "send_message",
        message: messageInput.value,
        time: new Date().getTime().toString(10)
    }));

    messageInput.value = "";
}

function renderMessage(message) {
    messageList.innerHTML += `
        <div class="post">
            <small><strong>anonymous - ${new Date(+ message.time).toLocaleString("en-GB", { hour12: true })}</strong></small>
            <div>${message.message}</div>
        </div>
    `;
}

function connect() {
    // TODO: Set string parameter to the WebSocket URL created when you create the API Gateway - starting with wss://...
    websocket = new WebSocket("");
    
    websocket.onopen = () => {
        console.debug("Websocket connected.");
        websocket.send(JSON.stringify({ action: "get_messages" }));
    };
    
    websocket.onmessage = e => {
        console.debug(e.data);
        
        const data = JSON.parse(e.data);
        
        if (data.messageType === "all_messages") {
            const messages = data.data;
            messageList.innerHTML = "";
            messages.forEach(message => renderMessage(message));
        } else {
            renderMessage(data);
        }
    };
}

connect();
