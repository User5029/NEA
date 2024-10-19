const {QUEUE} = require('./queue')
 

class CLIENT extends QUEUE{
    constructor() {
      super()
      this.show_id = null   
      this.config = {}          
    }
  }


module.exports = {CLIENT}