//const prompts = require('prompts')

const term = require('serverline')
const { database } = require('../index')

let commands = []

class TERMINAL {
    constructor() {
        // this.client = client;
        // this.database = database;
        // this.websocket = websocket;
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
}


module.exports = { TERMINAL, term }