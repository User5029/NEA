const wss = require("ws");


class WEBSOCKET {
    constructor(client) {
        this.client = client
        this.websocket = new wss.Server({port: 8080}, () => {
            console.log("[WebSocket] Server online")
        })
    }
}


module.exports = {WEBSOCKET}