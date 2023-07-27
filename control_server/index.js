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
      if(counter === 0){
         ws.send('c:/music/test2.mp3');
         counter = counter + 1
      } else if(counter === 1){
         ws.send('c:/music/test.mp3')
         counter = 0
      }
   })
})
wss.on('listening', () => {
   console.log('listening on 8080');
})

wss.on('error', (data) => {
   console.log('Client disconnected.')
})