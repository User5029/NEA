//const mysql = require('mysql')
const sqlite3 = require('sqlite3').verbose()
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
    this.db = new sqlite3.Database('./db.sqlite3')

    this.#init()
    this.show_create("test")
  }


  /**
   * This function executes in the background to hide the task from the main program
   * The '#' before the name of the function makes it a private function 
   */
  async #init() {
    const dataSql = fs.readFileSync('./src/functions/data.sql').toString();
    const dataArr = dataSql.toString().split(');');

    this.db.serialize(() => {
      // db.run runs your SQL query against the DB
      this.db.run('PRAGMA foreign_keys=OFF;');
      this.db.run('BEGIN TRANSACTION;');
      // Loop through the `dataArr` and db.run each query
      dataArr.forEach((query) => {
        if(query) {
          // Add the delimiter back to each query before you run them
          // In my case the it was `);`
          query += ');';
          this.db.run(query, (err) => {
             if(err) throw err;
          });
        }
      });
      this.db.run('COMMIT;');
    });
  }

  /** 
   * This function allows for general queries where required.
   * This function will not be used as it provided a point for SQL injection
  */
  async query(query) {
    this.db.all(query, [], (err, rows) => {
      if (err) {
        console.log(err)
        throw err
      }
      return rows
    })
  }

  /**
   * All the show table related SQL queries
   */

  async show_getId(name) {
    this.db.all(`SELECT * FROM show WHERE show_name = '${name}'`, [], (err, rows) => {
      if (err) {
        console.log(err)
        throw err
      }
      if (rows.length > 0){
        return rows[0]._id
      } else {
        return null
      }
    })
  }

  async show_getName(id) {
    this.db.all(`SELECT * FROM show WHERE _id = '${id}'`, [], (err, rows) => {
      if (err) {
        console.log(err)
        throw err
      }
      if (rows.length > 0){
        return rows[0].show_name
      } else {
        return null
      }
    })
  }

  async show_create(name) {
    // Return showId
    this.db.all(`INSERT INTO show (show_name) VALUES (?)`, [name], (err, rows) => {
      if(err){
        console.log(err)
        throw err
      }
    })
    this.db.all(`SELECT _id FROM show WHERE show_name = ?`, [name], (err, rows) => {
      if(err){
        console.log(err)
        throw err
      }
      return rows[0]._id
    })

  }

  async show_delete(id, name) {
    // Deletes everything from the database when a show gets deleted

    //Below checks that the name of the show matches the id
    if (this.show_getName(id) !== name) return "Error, name does not match id"
    this.db.all(`DELETE FROM cue WHERE show_id = ?`, [id], (err) => {
      if(err){
        console.log(err)
        throw(err)
      }
    })
    this.db.all(`DELETE FROM midi WHERE show_id = ?`, [id], (err) => {
      if(err){
        console.log(err)
        throw(err)
      }
    })
    this.db.all(`DELETE FROM audio WHERE show_id = ?`, [id], (err) => {
      if(err){
        console.log(err)
        throw(err)
      }
    })
    this.db.all(`DELETE FROM show WHERE show_id = ?`, [id], (err) => {
      if(err){
        console.log(err)
        throw(err)
      }
    })

    return true

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