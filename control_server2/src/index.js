/*
Imports all the managers and client needed to run the program
*/
const {DB} = require('./functions/database')
const {CLIENT} = require('./functions/client')
const {WEBSOCKET} = require('./functions/websocket')

/*
Sets up the clients by passing various variables that may be required
*/

const client = new CLIENT()
client.config = require('./config.json')
const database = new DB(client)
const WebSocket = new WEBSOCKET(client)

/**
 * The rest of the code for the 
 */

async function start() {
  await database.connect()
}

start()

database.DBQuery(`INSERT INTO NEA.show (show_name) VALUES (?);`, ");DROP TABLE show;--")
