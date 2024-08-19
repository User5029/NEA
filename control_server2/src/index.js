/*
Imports all the managers and client needed to run the program
*/
const { DB } = require('./functions/database')
const { CLIENT } = require('./functions/client')
const { WEBSOCKET } = require('./functions/websocket')
const { HASHING } = require('./functions/hashing')

/*
Sets up the clients by passing various variables that may be required
*/

const hash = new HASHING()
const client = new CLIENT()
//client.config = require('./config.json')
const database = new DB(client)
//const WebSocket = new WEBSOCKET(client, database)

setTimeout(async () => {
  //console.log(await database.show_create("Bob"))
  //console.log(await database.show_getName(4))
  //console.log(await database.show_getId("juhiudfhihi"))
  //console.log(await database.show_getName(46879756))
  console.log(await database.audio_createCue(11, "C:/abc.test"))
}, 1000)


async function test() {
  let reply = await hash.hash("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
  console.log(reply)
}




/**
 * The rest of the code for the application goes here
 */


// Function done when the program initially starts
async function start() {
  //await DB.connect() // Establishes a connection to the database.
}

start()

//database.DBQuery(`INSERT INTO NEA.show (show_name) VALUES (?);`, ");DROP TABLE show;--")
