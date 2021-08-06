set sql_safe_updates = 0;
drop database if exists nc_chase_2;
create database nc_chase_2;
use nc_chase_2;
drop table if exists year9, year10, year11, year12,
                     opt_out, caught, reassign, all_players;
create table all_players (
	id int primary key auto_increment not null,
    fname varchar(20),
    lname varchar(40),
    email varchar(64),
    form varchar(4),
    house varchar(10),
	game_id varchar(4),
	runner_id varchar(4),
	chaser_count int DEFAULT 0,
	reassign_counts int default 0,
	caught_counts int default 0,
	game_status int default 0);

load data infile "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Chase21.csv"
into table all_players 
lines terminated by '\r\n'
ignore 1 rows
(Fname, Lname, email, form, house);

delete from all_players where house not in ("Matai", "Rimu", "Totara", "Kowhai");

create table opt_out
(id int primary key auto_increment,
time_stamp datetime default current_timestamp,
email varchar(60) not null);

create table reassign
(id int primary key auto_increment,
time_stamp datetime default current_timestamp,
year_level INT not null,
game_id varchar(4) not null,
handled boolean DEFAULT 0);

create table caught
(id int primary key auto_increment,
time_stamp datetime default current_timestamp,
chaser_id varchar(4) not null,
runner_id varchar(4) not null,
valid boolean);