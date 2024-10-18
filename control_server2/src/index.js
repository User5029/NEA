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
  console.log("rest of program")
  main()
}, 1500);


// async function test() {
//   let reply = await hash.hash("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
//   console.log(reply)
// }





/**
 * The rest of the code for the application goes here
 */

async function main() {
  console.log(client.show_id)
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
            let loadData = database.query(`SELECT filePath FROM audio WHERE show_id = ?`, [client.show_id])
            let i = 0
            while(i < length(loadData)){

            }


            

          
      }
      }
  }
}

