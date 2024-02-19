const mysql = require('mysql')
const fs = require('fs')


class DB {
    constructor(host, username, password, database) {
      this.establishedConnection = null;
      this.host = host;
      this.username = username;      
      this.password = password;
      this.databse = database;
    }
  
    connection() {
      return new Promise((resolve, reject) => {
        resolve(mysql.createConnection({
          host: this.host,
          user: this.username,
          password: this.password,
          database: this.database,
        }))
      })
    }
  
    connect() {
      if (!this.establishedConnection) {
        this.establishedConnection = this.connection().then(res => {
          res.connect(function(err) {
            if (err) {
              this.dropConnection();
              throw err;
            }
            
            console.log(res.state, "connected")
          })
        });
      }
      const sqldata = fs.readFileSync('./src/functions/data.sql').toString()
      console.log(sqldata)
    }
  
    dropConnection() {
      if (this.establishedConnection) {
        this.establishedConnection.then(res => {
          res.end();
          console.log(res.state, 'connection dropped');
        });
        
        this.establishedConnection = null;
      }
    }
  }

module.exports = {DB}