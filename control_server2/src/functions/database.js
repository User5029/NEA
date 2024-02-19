const mysql = require('mysql')
const fs = require('fs')
const { promisify } = require('util')

class DB {
  // This is executed when the class is first added to the 
  constructor(client) {
    this.establishedConnection = null;
    this.client = client // Allows anything in the client object to be refernced in this class


    // Creates the database configuration using the config provided by the client class
    this.connection = mysql.createConnection({
      host: this.client.config.mariadb.host,
      user: this.client.config.mariadb.user,
      password: this.client.config.mariadb.password,
      database: this.client.config.mariadb.database

    })
  }

  // Function to create the database connection and will perform some prechecks before the user starts
  connect() {
    this.connection.connect(function (err) {
      if (err) {
        console.error(`[Database] Error Connecting` + err.stack);
        return;
      }
      console.log(`[Database] Connected`);
    });

    this.DBQuery = promisify(this.connection.query).bind(this.connection)

    this.init() // Makes sure that the database schema is in place so that the program does not crash when the schema is not present.
  }

  async init() {
    const dataSql = fs.readFileSync("./src/functions/data.sql", "utf-8"); // Gets the data from the file and decodes using utf-8
    const queries = dataSql.split(';'); // Splits whole schema into smaller schemas to be executed individually
    // cycles through all the table schemas and executes the query
    queries.forEach((query) => {
      if (query.trim() !== '') {
        this.connection.query(query, (error, results, fields) => {
          if (error) throw error; // Voids any errors so that the program does not crash
        });
      }
    })
  }

  async query(query) {
    let data = await this.DBQuery(query)
    return data
  }
}

module.exports = { DB }