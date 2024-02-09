const mariadb = require("mysql");
const ws = require("ws");

class client{
    constructor() {
    }
}
client.config = require("./config.json")

const wss = new WebSocket.Server({ port: 8080 }, () => {
  console.log("[WebSocket] Sever Online");
});
var connection = mariadb.createConnection({
  host:     client.config.mariadb.host,
  user:     client.config.mariadb.user,
  password: client.config.mariadb.pass,
  database: client.config.mariadb.db
})
connection.connect(function(err) {
    if(err) {
        console.error("[Database] Error connecting to the database: " + err.stack);
        return;        
    }
    console.log(`[Database] Connected, ID ${connection.threadId}`)
})
