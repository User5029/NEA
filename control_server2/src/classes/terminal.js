//const prompts = require('prompts')

const term = require('serverline')

let commands = []



class TERMINAL {
    constructor(client, database, websocket) {
        this.client = client;
        this.datsabase = database;
        this.websocket = websocket;
        this.#init()
    }

    async #init() {
        let show_cmds = ['show', 'show create', 'show load', 'show delete', 'show list']


        for (const i of show_cmds) {
            commands.push(i)
        }

        term.init()
        term.setCompletion(commands)
        term.setPrompt('> ')
    }

    async show(_cmd){
        console.log(_cmd)
        _cmd = _cmd.shift(1)
        console.log(_cmd)
    }

    async ask(question) {
    }


}


module.exports = { TERMINAL, term}