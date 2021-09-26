-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- DATABASE mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- DATABASE nc_chase
-- -----------------------------------------------------

-- -----------------------------------------------------
-- DATABASE nc_chase
-- -----------------------------------------------------

DROP DATABASE IF EXISTS `nc_chase` ;
CREATE DATABASE IF NOT EXISTS `nc_chase` DEFAULT CHARACTER SET utf8 ;
USE `nc_chase`;

-- -----------------------------------------------------
-- Table `nc_chase`.`all_players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nc_chase`.`all_players` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NULL DEFAULT NULL,
  `lname` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(64) NOT NULL,
  `form` VARCHAR(4) NULL DEFAULT NULL,
  `year_level` INT GENERATED ALWAYS AS (substr(`form`,1,2)) STORED,
  `house` VARCHAR(6) NULL DEFAULT NULL,
  `chaser_id` VARCHAR(4) NULL DEFAULT NULL,
  `runner_id` VARCHAR(4) NULL DEFAULT NULL,
  `game_status` VARCHAR(7) NULL DEFAULT 'alive',
  `chaser_count` INT NULL DEFAULT '0',
  `caught_count` INT NULL DEFAULT '0',
  `reassign_count` INT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `chaser_id_UNIQUE` (`chaser_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Chase21.csv"
INTO TABLE all_players
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(fname, lname, email, form, house);

SET SQL_SAFE_UPDATES = 0;
DELETE FROM all_players WHERE house NOT IN ("Matai", "Rimu", "Totara", "Kowhai");
DELETE FROM all_players WHERE year_level = 13;
SET SQL_SAFE_UPDATES = 1;

-- -----------------------------------------------------
-- Table `nc_chase`.`caught`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nc_chase`.`caught` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `timestamp` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `chaser_id` VARCHAR(4) NOT NULL,
  `runner_id` VARCHAR(4) NOT NULL,
  `valid` TINYINT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `nc_chase`.`opt_out`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nc_chase`.`opt_out` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `timestamp` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `email` VARCHAR(64) NOT NULL,
  `reasons` LONGTEXT NULL DEFAULT NULL,
  `valid` TINYINT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `nc_chase`.`reassign`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nc_chase`.`reassign` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `timestamp` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `chaser_id` VARCHAR(4) NOT NULL,
  `fname` VARCHAR(20) NOT NULL,
  `valid` TINYINT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `nc_chase`.`report`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nc_chase`.`report` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `timestamp` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `email` VARCHAR(64) NOT NULL,
  `message` TEXT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;