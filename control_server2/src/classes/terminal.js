//const prompts = require('prompts')

const term = require('serverline')

class TERMINAL {
    constructor(client) {
        this.client = client;
        term.init()
        term.setPrompt('> ')
    }

    async write(text){
        process.stdout.write(`${text}\n`);     
        
    }

    async ask(question){
    }


}


module.exports = {TERMINAL}