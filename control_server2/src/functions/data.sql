CREATE TABLE IF NOT EXISTS show (
    _id varchar(255) PRIMARY KEY AUTOINCREMENT,
    show_name varchar(255) NOT NULL
)

CREATE TABLE IF NOT EXISTS cue_table (
    _id varchar(255) PRIMARY KEY AUTOINCREMENT,
    show_id varchar(255) FOREIGN KEY REFERENCES show(_id),
    cue_number int(255),
    audio_cue varchar(255) FOREIGN KEY REFERENCES audio_table(_id),
    midi_cue varchar(255) FOREIGN KEY REFERENCES,
    notes varchar(255) FOREIGN KEY REFERENCES ,
    
)

CREATE TABLE IF NOT EXISTS audio_table (
    _id varchar(255) PRIMARY KEY AUTOINCREMENT,
    show_id varchar(255) FOREIGN KEY REFERENCES show(_id),
    file_path varchar(255) NOT NULL,
    prewait float(16) DEFAULT 0,
    fadeIn float(16) DEFAULT 0,
    fadeOut float(16) DEFAULT 0,
    postWait float(16) DEFAULT 0,
    volume float(8) DEFAULT 0.9
)

CREATE TABLE IF NOT EXISTS midi_cue (
    _id varchar(255) PRIMARY KEY AUTOINCREMENT,
    show_id varchar(255) FOREIGN KEY REFERENCES show(_id),
)

CREATE TABLE IF NOT EXISTS notes (
    _id varchar(255) PRIMARY KEY AUTOINCREMENT,
    show_id varchar(255) FOREIGN KEY REFERENCES show(_id),
    note TEXT(65535)
)