drop table if exists competitions cascade;
drop table if exists seasons cascade;

create table if not exists competitions (
	competition_id int not null primary key,
	country_name varchar(30) not null, -- TODO: Reference countries
	competition_name varchar(30) not null,
	competition_gender varchar(8),
	competition_youth boolean,
	competition_international boolean
);

create table if not exists seasons (
	season_id int not null,
	season_name varchar(10) not null,
	competition_id int references competitions(competition_id)
);

create table if not exists countries (
	country_id int primary key,
	name varchar(30)
);

create table if not exists managers (
	manager_id int primary key,
	name varchar(30),
	nickname varchar(30),
	dob date,
	country_id int references countries(country_id)
);

create table if not exists competition_stages (
	competition_stage_id int primary key,
	name varchar(10)
);

create table if not exists stadiums (
	stadium_id int primary key,
	name varchar(30),
	country_id int references countries(country_id)
);

create table if not exists referees (
	referee_id int primary key,
	name varchar(30),
	country_id int references countries(country_id)
);
create table if not exists matches (
	match_id int not null primary key,
	match_date date,
	kick_off time,
	competition int references competitions(competition_id),
	season int references seasons(season_id),
	home_team_id int references teams(team_id),
	away_team_id int references teams(team_id),
	home_score int,
	away_score int,
	match_week int,
	competition_stage int references competition_stages(competition_stage_id),
	stadium_id int references stadiums(stadium_id),
	referee_id int references referees(referee_id)
);

create table if not exists teams (
	team_id int primary key,
	team_name varchar(30),
	team_gender varchar(8),
	team_group int, -- TODO: Figure out what this is
	country_id int references countries(country_id)
);

create table if not exists team_managers (
	team_id int references teams(team_id),
	manager_id int references managers(manager_id)
);

create table if not exists position (
	id int not null primary key,
	name varchar(80) not null
);

create table if not exists players (
	id int not null primary key,
	name varchar(80) not null,
	position int references position(id),
	jersey_number int not null
);
