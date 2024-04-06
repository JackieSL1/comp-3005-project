drop table if exists 
competitions,
countries,
managers,
competition_stages,
stadiums,
referees,
matches,
teams,
team_managers,
cards,
positions,
players,
lineups,
cascade;

create table if not exists competitions (
	competition_id int not null,
	season_id int not null,
	season_name varchar(30) not null,
	country_name varchar(30) not null, -- TODO: Reference countries
	competition_name varchar(30) not null,
	competition_gender varchar(8),
	competition_youth boolean,
	competition_international boolean,
	primary key (competition_id, season_id)
);

/*
create table if not exists seasons (
	season_id int not null,
	season_name varchar(30) not null,
);
*/

create table if not exists countries (
	country_id int primary key,
	name varchar(40)
);

create table if not exists managers (
	manager_id int primary key,
	name varchar(40),
	nickname varchar(30),
	dob date,
	country_id int references countries(country_id)
);

create table if not exists competition_stages (
	competition_stage_id int primary key,
	name varchar(30)
);

create table if not exists stadiums (
	stadium_id int primary key,
	name varchar(80),
	country_id int references countries(country_id)
);

create table if not exists referees (
	referee_id int primary key,
	name varchar(40),
	country_id int references countries(country_id)
);


create table if not exists teams (
	team_id int primary key,
	team_name varchar(30),
	team_gender varchar(8),
	team_group int, -- TODO: Figure out what this is
	country_id int references countries(country_id)
);

create table if not exists matches (
	match_id int not null primary key,
	match_date date,
	kick_off time,
	competition_id int not null,
	season_id int not null,
	home_team_id int references teams(team_id),
	away_team_id int references teams(team_id),
	home_score int,
	away_score int,
	match_week int,
	competition_stage_id int references competition_stages(competition_stage_id),
	stadium_id int references stadiums(stadium_id),
	referee_id int references referees(referee_id),
	foreign key (competition_id, season_id) references competitions(competition_id, season_id)
);


create table if not exists team_managers (
	team_id int references teams(team_id),
	manager_id int references managers(manager_id)
);

create table if not exists players (
	player_id int primary key,
	player_name varchar(80) not null,
	player_nickname varchar(30),
	jersey_number int not null,
	country int references countries(country_id)
);

create table if not exists cards (
	player_id int references players(player_id),
	match_id int references matches(match_id),
	time varchar(30),
	card_type varchar(30),
	reason varchar(30),
	"period" int
);

create table if not exists positions (
	player_id int references players(player_id),
	match_id int references matches(match_id),
	position_id int,
    "position" varchar(50) not null,
    "from" varchar(10) not null, -- This might need to be a time
    "to" varchar(10),
    from_period int not null,
    to_period int,
    start_reason varchar(40) not null,
    end_reason  varchar(40) not null
);

create table if not exists lineups (
	match_id int references matches(match_id),
	team_id int references teams(team_id),
	player_id int references players(player_id)
);
