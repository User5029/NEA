//const mariadb = require("mysql");
const WebSocket = require("ws");

class client {
  constructor() {
      
  }
}

client.config = require("./config.json")

const wss = new WebSocket.Server({ port: 8080 }, () => {
  console.log("[WebSocket] Sever Online");
});

const {DB} = require('./functions/database')


const database = new DB(client.config.mariadb.host, client.config.mariadb.user, client.config.mariadb.password, client.config.mariadb.database)
database.connect()
database.connection()