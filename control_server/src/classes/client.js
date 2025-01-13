const {QUEUE} = require('./queue')
 
/*
This class inherits all the properties from the Queue class by using the ‘extends’ keyword. This is saying the CLIENT class is an extension of the QUEUE class.
*/
class CLIENT extends QUEUE{
    constructor() {
      super()
      this.show_id = null   
      this.config = {}          
    }
  }


module.exports = {CLIENT}
