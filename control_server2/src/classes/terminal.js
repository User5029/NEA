const prompts = require('prompts')



class TERMINAL {
    constructor() {
        process.stdout.write("Terminal Online\n");
    }

    async write(text){
        process.stdout.write(`${text}\n`);     
        
    }

    async ask(question){
        const response = await prompts({
            type: 'text',
            name: 'question',
            message: question
        });

        return response.question
    }


}


module.exports = {TERMINAL}