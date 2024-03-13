const wss = require("ws");


class WEBSOCKET {
    constructor(client, database) {
        this.client = client
        this.database = database
        this.myId = "001"
        this.websocket = new wss.Server({port: 8080}, () => {
            console.log("[WebSocket] Server online")
        })

        this.websocket.on('connection', async function(ws) {
            console.log("Client Connected")

            ws.on('message', (data, isBinary) => {
                const message = isBinary ? data : data.toString();
                let cmd = message.split(',')

                if(!cmd === this.myId) return;

                let send = this.getCommand(message)

                ws.send(send)
                


            })

        })
    }

    getCommand(_msg){
        let command = _msg[3]
        
        
        // Splits the command to their command manager as this makes it easier to debug the code
        switch(command) {
            
            case "CUEREQ":
                return this.cueAudioManager(_msg)
            
        }

    }

    // Deal with all the incomming requests with the audioCue
    cueAudioManager(_msg){
        let subcommand = _msg[4]

        switch(subcommand) {
            // Gets the audio source requested
            case "REQUEST":
                let request = this.database.audio_GetCue(_msg[5])
                console.log(request)

                //return this.queSender(_msg[0],'audio','arm',_msg[4])
        }

    }




    queSender(to, command, subcommand, channel, cueNum, cueName, audioUrl, preWait, fadeIn, fadeOut, postWait){
        // Maybe inject some default values here
        let msg = `${to},${this.myId},${command},${subcommand},${channel},${cueNum},${cueName},${audioUrl},${preWait},${fadeIn},${fadeOut},${postWait}`
    }
}



module.exports = {WEBSOCKET}