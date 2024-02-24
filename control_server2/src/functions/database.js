const mysql = require('mysql')
const fs = require('fs')
const { promisify } = require('util')

/**
 * TODO: Add SQL injection protection (maybe regex?)
 * TODO: Parameterized queries
 * TODO: Multi query detection
 * 
 * Look at https://github.com/boyzoid/sql-template-tag-demo/blob/main/src/index.js for ideas
 */

/** 
 * Functions to program
 * [Show] Get by name
 * [Show] Get by Id
 * [Show] Exists
 * [Cue] Get Cue
 * [Cue] Create Cue
 * [Cue] Get cue by id
 */

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


    // Usage
    // const userInput = "Alice'; DROP TABLE users;";
    // const sanitizedInput = this.connection.escape(userInput)
    // console.log("Sanitized input:", sanitizedInput); 

    this.#init() // Makes sure that the database schema is in place so that the program does not crash when the schema is not present.
  }

  /**
   * This function executes in the background to hide the task from the main program
   * The '#' before the name of the function makes it a private function 
   */
  async #init() {
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

  /** 
   * This function allows for general queries where required.
   * This function will not be used as it provided a point for SQL injection
  */
  async query(query) {
    let data = await this.DBQuery(query)
    return data
  }

  /**
   * All the show table related SQL queries
   */

  async show_getId(name) {

  }

  async show_getName(id) {

  }

  async show_create(name) {
    // Return showId

  }

  async show_delete(id, name) {
    // Delete all other entries in the database related to that show? 
  }

  /**
   * All the audio table related queries
  */

  async audio_getCue(_id, showId) {
    // Return all the config for that audioCue
  }

  async audio_createCue(showId, filePath) {
    // Return cue id
  }

  async audio_deleteCue(_id, showId) {

  }

  async audio_updateFilePath(_id, newFilePath) {

  }

  async audio_updatePreWait(_id, preWait) {

  }

  async audio_updateFadeIn(_id, fadeIn) {

  }

  async audio_updateFadeOut(_id, fadeOut) {

  }

  async audio_updatePostWait(_id, postWait) {

  }

  async audio_updateVolume(_id, volume) {

  }

  /**
   * For all the midi cue's SQL queries
   */

  async midi_getCue(_id, showId) {
    // Return all values
  }

  





}

module.exports = { DB }