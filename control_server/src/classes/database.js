//const mysql = require('mysql')
const sqlite3 = require('sqlite3').verbose()
const fs = require('fs')
const { promisify } = require('util')

/**
 * DONE: Add SQL injection protection (maybe regex?)
 * DONE: Parameterized queries
 * TODO: Add better error messages
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
    this.db = new sqlite3.Database('./src/data/db.sqlite3', (err) => {
      if (err) {
        console.log(err)
        throw err
      }
      console.log("Connected to the SQlite database.");
    })

    this.#init()
  }


  /**
   * This function executes in the background to hide the task from the main program
   * The '#' before the name of the function makes it a private function 
   */
  async #init() {
    const dataSql = fs.readFileSync('./src/data/data.sql').toString();
    const dataArr = dataSql.toString().split(');');

    this.db.serialize(() => {
      // db.run runs your SQL query against the DB
      this.db.run('PRAGMA foreign_keys=OFF;');
      this.db.run('BEGIN TRANSACTION;');
      // Loop through the `dataArr` and db.run each query
      dataArr.forEach((query) => {
        if (query) {
          // Add the delimiter back to each query before you run them
          // In my case the it was `);`
          query += ');';
          this.db.run(query, (err) => {
            if (err) throw err;
          });
        }
      });
      this.db.run('COMMIT;');
    });
  }

  /** 
   * This function allows for general queries where required.
   * This is also using parametised queries to reduce the chance of SQL injection
   * 
   * This function will only return one result to the other function (makes it easier) 
  */
  async query(query, paramsArr = []) {
    const that = this;
    return new Promise(function (resolve, reject) {
      that.db.all(query, paramsArr, function (error, result) {
        if (error) {
          console.log(error)
          reject(error);
        } else {
          resolve(result[0]);
        }
      });
    });
  }

  /**
   * This function returns all values in an array which will be useful for some functions
   * This function also uses parametized queries for the same reasons.
   */

  async queryAll(query, paramsArr = []) {
    const that = this;
    return new Promise(function (resolve, reject) {
      that.db.all(query, paramsArr, function (error, result) {
        if (error) {
          reject(error);
        } else {
          resolve(result);
        }
      });
    });
  }

  /**
   * MISC Functions
   */

  async getLastId() {
    let err, result = await this.query(`SELECT last_insert_rowid()`)
    if (err) {
      console.log(err)
      throw (err)
    }

    let json = JSON.stringify(result)
    json = json.split(':')
    json = json[1].replace('}', '')
    return json
  }

  /**
   * All the show table related SQL queries
   */

  async show_getId(name) {
    if (!name) return;
    name = name.toLowerCase()
    let err, result = await this.query(`SELECT * FROM show WHERE show_name = ?`, [name])
    if (err) {
      console.log(err)
      throw err
    }
    let result2 = result ?? { _id: null }
    return result2._id
  }

  async show_getName(id) {
    if (!id) return;
    let err, result = await this.query(`SELECT * FROM show WHERE _id = ?`, [id])
    if (err) {
      console.log(err)
      throw err
    }
    let result2 = result ?? { show_name: null }
    return result2.show_name
  }

  async show_create(name) {
    if (!name) return;
    name = name.toLowerCase()

    let existingId = await this.show_getId(name)

    if (existingId !== null) return existingId

    let err = await this.query(`INSERT INTO show (show_name) VALUES (?)`, [name])
    if (err) {
      console.log(err)
      throw err
    }

    existingId = await this.show_getId(name)
    return existingId


  }

  async show_delete(id, name) {
    if (!id || !name) return;


    //Below checks that the name of the show matches the id (basic check)
    if (this.show_getName(id) !== name) return "Error, name does not match id"

    await this.query(`DELETE FROM cue WHERE show_id = ?`, [id])
    await this.query(`DELETE FROM midi WHERE show_id = ?`, [id])
    await this.query(`DELETE FROM show WHERE _id = ?`, [id])
    await this.query(`DELETE FROM audio WHERE show_id = ?`, [id])

    return true
  }

  async show_listall() {

    let err, res = await this.query('SELECT show_name FROM show')
    if (err) {
      console.log(err)
      throw err
    } else {
      return res
    }

  }

  /**
   * All cues in general
   */

  async cue_getAll(showId) {
    if (!showId) return -1

    let err, result = await this.queryAll(`SELECT * FROM audio WHERE show_id = ? `, [showId])
    if (err) {
      console.log(err)
      throw err
    }
    return result
  }

  async cue_getId(showId, cueNum) {
    if (!showId || !cueNum) return;

    let err, result = await this.query(`SELECT * FROM cue WHERE show_id = ? AND cueNumber = ?`, [showId, cueNum])
    if (err) {
      console.log(err)
      throw err
    }
    let result2 = result ?? { _id: null }
    return result2._id

  }

  async cue_getCueById(cueId) {
    if (!cueId) return;

    let err, result = await this.query(`SELECT * FROM cue WHERE _id = ?`, [cueId])
    if (err) {
      console.log(err)
      throw err
    }
    let result2 = result ?? null
    return result2

  }

  async cue_create(data, showId) {
    if (!data || !showId) return -1

    let cueNum = data.cueNum ?? null
    let cueName = data.cueName ?? "Unnamed"
    let audCueId = data.audCueId ?? null

    if (cueNum === null) {
      console.log(`[DB] Unable to create cue, cue number not provided`)
      return -1
    }

    await this.query(`INSERT INTO cue (show_id, cueNumber, cueName, audioCue) VALUES (?,?,?,?)`, [showId, cueNum, cueName, audCueId])

    return await this.cue_getId(showId, cueNum)

  }

  async cue_delete(_id) {
    if (!_id) return;

    let err = await this.query(`DELETE FROM cue WHERE _id = ?`, [_id])
    if (err) {
      console.log(err)
      throw err
    }

    return true
  }

  /**
   * All the audio table related queries
  */

  async audio_getCue(_id, showId) {
    if (!_id || !showId) return;

    let err, result = await this.query(`SELECT * FROM audio WHERE _id = ? AND show_id = ?`, [_id, showId])
    if (err) {
      console.log(err)
      throw err
    }
    return result
  }

  async audio_getAllCues(showId) {
    if (!showId) return;

    let err, result = await this.queryAll(`SELECT * FROM audio WHERE AND show_id = ?`, [showId])
    if (err) {
      console.log(err)
      throw err
    }
    return result
  }

  async audio_createCue(showId, filePath, preWait = 0, fadeIn = 0, fadeOut = 0, postWait = 0, volume = 0.8) {
    if (!showId || !filePath) return;

    let err = await this.query(`INSERT INTO audio (show_id, filePath, preWait, fadeIn, fadeOut, postWait, volume) VALUES (?,?,?,?,?,?,?)`, [showId, filePath, preWait, fadeIn, fadeOut, postWait, volume])
    if (err) {
      console.log(err)
      throw err
    }

    return this.getLastId()

  }

  async audio_deleteCue(_id, showId) {
    if (!_id || !showId) return;

    let err = await this.query(`DELETE FROM audio WHERE _id = ? AND show_id = ?`, [_id, showId])

    if (err) {
      console.log(err)
      throw err
    }
    return true

  }

  async audio_updateFilePath(_id, newFilePath) {
    if (!_id || !newFilePath) return;

    let err = await this.query(`UPDATE audio SET filePath = ? WHERE _id = ? `, [newFilePath, _id])
    if (err) {
      console.log(err)
      throw (err)
    }
    return true
  }

  async audio_updatePreWait(_id, preWait) {
    if (!_id || !preWait) return;

    let err = await this.query(`UPDATE audio SET preWait = ? WHERE _id = ? `, [preWait, _id])
    if (err) {
      console.log(err)
      throw (err)
    }
    return true

  }

  async audio_updateFadeIn(_id, fadeIn) {
    if (!_id || !fadeIn) return;

    let err = await this.query(`UPDATE audio SET fadeIn = ? WHERE _id = ? `, [fadeIn, _id])
    if (err) {
      console.log(err)
      throw (err)
    }
    return true

  }

  async audio_updateFadeOut(_id, fadeOut) {
    if (!_id || !fadeOut) return;

    let err = await this.query(`UPDATE audio SET fadeOut = ? WHERE _id = ? `, [fadeOut, _id])
    if (err) {
      console.log(err)
      throw (err)
    }
    return true

  }

  async audio_updatePostWait(_id, postWait) {
    if (!_id || !postWait) return;

    let err = await this.query(`UPDATE audio SET postWait = ? WHERE _id = ? `, [postWait, _id])
    if (err) {
      console.log(err)
      throw (err)
    }
    return true

  }

  async audio_updateVolume(_id, volume) {
    if (!_id || !volume) return;

    let err = await this.query(`UPDATE audio SET volume = ? WHERE _id = ? `, [volume, _id])
    if (err) {
      console.log(err)
      throw (err)
    }
    return true

  }



}

let a = true

module.exports = { DB }