/*
Imports all the managers and client needed to run the program
*/
const { DB } = require('./classes/database')
const { CLIENT } = require('./classes/client')
const { WEBSOCKET } = require('./classes/websocket')
const { HASHING } = require('./classes/hashing')
const { TERMINAL, term } = require('./classes/terminal')
const utils = require('./utils/utils')
const fs = require('fs')

/*
Sets up the clients by passing various variables that may be required
*/

const hash = new HASHING()
const client = new CLIENT()
const database = new DB(client)
const WebSocket = new WEBSOCKET(client, database)
const terminal = new TERMINAL(client, database, WebSocket)

setTimeout(async () => {
  term.on('line', function (line) {
    line = line.toLowerCase()
    //console.log('CMD: ' + line)
    line = line.split(' ')
    TermCommands(line)
  }, 100)

  term.on('SIGINT', function (rl) {
    rl.question('Confirm exit (y/N): ', (answer) => answer.match(/^y(es)?$/i) ? process.exit(0) : rl.output.write('\x1B[1K> '))
  })
}, 100)

setTimeout(() => {
  const WebSocket = require('ws')
const wss = new WebSocket.Server({ port: 8080 }, () => {
   console.log('server started')
})

let counter = 0
wss.on('connection', function connection(ws) {
   console.log("Client Connected.")
   ws.on('message', (data, isBinary) => {
      const message = isBinary ? data : data.toString();
      let cmd = message.split(',');
      console.log(`To:${cmd[0]}, From: ${cmd[1]}, CMD: ${cmd[2]}`)

      console.log('data received \n %o', message);
      // setTimeout(() => {
      //    ws.send(message)
      // }, 1000)
      if (message === "001,002,CUEREQ,REQUEST,1,1") {
         ws.send('002,001,audio,arm,1,1,test,c:/a.mp3,0,0,5');
      }

      // if(counter === 0){
      //    ws.send('001,000,audio,arm,1,1,test,c:/music/test2.mp3,0,0,0,0');
      //    counter = counter + 1
      // } else if(counter === 1){
      //    ws.send('c:/music/test.mp3')
      //    counter = 0
      // }
   })
})
wss.on('listening', () => {
   console.log('listening on 8080');
})

wss.on('error', (data) => {
   console.log('Client disconnected.')
})
}, 1500);


// async function test() {
//   let reply = await hash.hash("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
//   console.log(reply)
// }







/**
 * The rest of the code for the application goes here
 */

async function main() {
  e('Query')
  e(await database.query('SELECT * FROM show'))
  e('Queryall')
  e(await database.queryAll('SELECT * FROM show'))
  e('Show Create')
  e(await database.show_create('test8556'))
  e('Get Last ID')
  e(await database.getLastId())
  e('Show list')
  e(await database.show_listall())
  e('ID of "Bob"')
  let tmpdata1 = await database.show_getId('Bob')
  e(tmpdata1)
  e(`Name of ID ${tmpdata1}`)
  e(await database.show_getName(tmpdata1))


    
}

async function e(_msg){
  console.log(_msg)
}


async function TermCommands(_cmd) {
  switch (_cmd[0]) {
    case 'show':
      if (_cmd[1] === undefined) {
        console.log(`The available sub commands are 'create' 'load' 'delete' 'list'`)
      } else {
        let data = null
        switch (_cmd[1]) {
          case 'create':
            let exists = await database.show_getId(_cmd[2])
            if (exists !== null) {
              console.log('[ERROR] A show already exists with this name')
            } else {
              let showId = await database.show_create(_cmd[2])
              client.show_id = showId
              console.log(`Your show: ${_cmd[2]} has a show ID of: ${showId}`)
            }
            break

          case 'list':
            data = await database.show_listall()
            console.log(data)
            break

          case 'load':
            if(!_cmd[2]) return console.log(`Please enter a show name to load`)
            data = await database.show_getId(_cmd[2])
            if(data !== null && data !== undefined){
              client.show_id = data
            } else {
              return console.log("This show does not exist please use 'show create' to make a show")
            }
            let loadData = await database.audio_getAllCues(client.show_id)
            console.log(loadData)
            console.log("Checking show data ... ")
            for(let tmpdata of loadData){
              if(!fs.existsSync(cueFile[2])){
                console.log(`File: ${cueFile}, does not exist error!`)
              } else {
                console.log(`Checks out`)
              }
            }

            console.log(`Data loaded successfully`)
            break

            

          
      }
      }
  }
}

