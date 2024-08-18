CREATE TABLE IF NOT EXISTS `show` (
	`_id` INT(100) NOT NULL AUTO_INCREMENT,
	`show_name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`_id`) USING BTREE
);

CREATE TABLE IF NOT EXISTS `audio` (
	`_id` INT(100) NOT NULL AUTO_INCREMENT,
	`show_id` INT(100) NOT NULL,
	`filePath` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`preWait` FLOAT NOT NULL DEFAULT '0',
	`fadeIn` FLOAT NOT NULL DEFAULT '0',
	`fadeOut` FLOAT NOT NULL DEFAULT '0',
	`postWait` FLOAT NOT NULL DEFAULT '0',
	`volume` FLOAT NOT NULL DEFAULT '0.9',
	PRIMARY KEY (`_id`) USING BTREE,
	INDEX `show_id` (`show_id`) USING BTREE,
	CONSTRAINT `show_id` FOREIGN KEY (`show_id`) REFERENCES `show` (`_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS `midi` (
	`_id` INT(100) NOT NULL AUTO_INCREMENT,
	`show_id` INT(100) NOT NULL,
	PRIMARY KEY (`_id`) USING BTREE,
	INDEX `showid` (`show_id`) USING BTREE,
	CONSTRAINT `showid` FOREIGN KEY (`show_id`) REFERENCES `show` (`_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS `notes` (
	`_id` INT(100) NOT NULL AUTO_INCREMENT,
	`show_id` INT(100) NOT NULL,
	`data` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`_id`) USING BTREE,
	INDEX `showid` (`show_id`) USING BTREE,
	CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`show_id`) REFERENCES `show` (`_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS `cue` (
	`_id` INT(100) NOT NULL AUTO_INCREMENT,
	`show_id` INT(100) NOT NULL,
	`cueNumber` INT(100) NOT NULL,
	`cueName` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
	`audioCue` INT(100) NULL DEFAULT NULL,
	`midiCue` INT(100) NULL DEFAULT NULL,
	`noteCue` INT(100) NULL DEFAULT NULL,
	PRIMARY KEY (`_id`) USING BTREE,
	INDEX `showid2` (`show_id`) USING BTREE,
	INDEX `audioid` (`audioCue`) USING BTREE,
	INDEX `midicue` (`midiCue`) USING BTREE,
	INDEX `notecue` (`noteCue`) USING BTREE,
	CONSTRAINT `audioid` FOREIGN KEY (`audioCue`) REFERENCES `audio` (`_id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `midicue` FOREIGN KEY (`midiCue`) REFERENCES `midi` (`_id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `notecue` FOREIGN KEY (`noteCue`) REFERENCES `notes` (`_id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `showid2` FOREIGN KEY (`show_id`) REFERENCES `show` (`_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);