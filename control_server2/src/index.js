/*
Imports all the managers and client needed to run the program
*/
const {DB} = require('./functions/database')
const {CLIENT} = require('./functions/client')

/*
Sets up the clients by passing various variables that may be required
*/
const client = new CLIENT()
client.config = require('./config.json')
const database = new DB(client)




const WebSocket = require("ws");




const wss = new WebSocket.Server({ port: 8080 }, () => {
  console.log("[WebSocket] Sever Online");
});


async function start() {
  await database.connect()
}

start()




