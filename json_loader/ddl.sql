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
	player_positions,
	players,
	lineups,
	event_types,
	event_tactics,
	related_events,
	events,
	ball_recovery,
	dispossessed,
	duel,
	camera_on,
	block,
	offside,
	clearance,
	interception,
	dribble,
	shot,
	pressure,
	half_start,
	substitution,
	own_goal_against,
	foul_won,
	foul_committed,
	goalkeeper,
	bad_behaviour,
	own_goal_for,
	player_on,
	player_off,
	shield,
	camera_off,
	pass,
	fifty_fifty,
	half_end,
	starting_xi,
	tactical_shift,
	error,
	miscontrol,
	dribbled_past,
	injury_stoppage,
	referee_ball_drop,
	ball_receipt,
	carry
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
	position_id int primary key,
    position varchar(50) not null
);

create table if not exists player_positions (
	player_id int references players(player_id),
	match_id int references matches(match_id),
	position_id int references positions(position_id),
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
	player_id int references players(player_id),
	jersey_number int not null
);

create table if not exists event_types (
	event_type_id int primary key,
	name varchar(30)
);

create table if not exists events (
	id uuid primary key,
	match_id int references matches(match_id),
	index int,
	period int,
	timestamp varchar(20), -- TODO: timestamp type instead?
	minute int,
	second int,
	event_type_id int references event_types(event_type_id),
	posession int,
	posession_team_id int references teams(team_id),
	play_pattern varchar(30),
	team_id int references teams(team_id),
	player_id int references players(player_id),
	position int references positions(position_id),
	location_x real,
	location_y real,
	duration real,
	under_pressure boolean,
	counterpress boolean,
	out boolean
);

create table if not exists event_tactics (
	event_id uuid references events(id),
	player_id int references players(player_id),
	position int references positions(position_id),
	jersey_number int not null
);

create table if not exists related_events (
	event_id uuid references events(id),
	related_event_id uuid references events(id)
);

-- EVENT TYPES
create table if not exists ball_recovery (
	event_id uuid references events(id),
	recovery_failure boolean,
	offensive boolean
);

create table if not exists shot (
	event_id uuid references events(id),
	statsbomb_xg double precision,
	end_location_x real,
	end_location_y real,
	end_location_z real,
	key_pass_id uuid references events(id),
	body_part varchar(30),
	type varchar(30),
	outcome varchar(30),
	first_time boolean,
	technique varchar(30),
	deflected boolean,
	one_on_one boolean,
	aerial_won boolean,
	saved_to_post boolean,
	redirect boolean,
	open_goal boolean,
	follows_dribble boolean,
	saved_off_target boolean
);

-- create table if not exists dispossessed ( <- DOESN'T NEED EXTRA FIELDS
-- 	event_id uuid references events(id),
	
-- );

create table if not exists duel (
	event_id uuid references events(id),
	type varchar(30),
	outcome varchar(30)
);
-- create table if not exists camera_on (
-- 	event_id uuid references events(id),
-- );
create table if not exists block (
	event_id uuid references events(id),
	deflection boolean,
	offensive boolean,
	save_block boolean
);
-- create table if not exists offside ( -- NO FIELDS
-- 	event_id uuid references events(id),
-- );
create table if not exists clearance ( 
	event_id uuid references events(id),
	body_part varchar(20)
);
create table if not exists interception (
	event_id uuid references events(id),
	outcome varchar(30)
);
create table if not exists dribble (
	event_id uuid references events(id),
	outcome varchar(30),
	overrun boolean,
	nutmeg boolean,
	no_touch boolean
);
-- create table if not exists pressure (
-- 	event_id uuid references events(id),
-- );
create table if not exists half_start (
	event_id uuid references events(id),
	late_video_start boolean
);
create table if not exists substitution (
	event_id uuid references events(id),
	outcome varchar(30),
	replacement int references players(player_id)
);
-- create table if not exists own_goal_against ( NO FIELDS
-- 	event_id uuid references events(id),
-- );
create table if not exists foul_won (
	event_id uuid references events(id),
	penalty boolean,
    defensive boolean,
    advantage boolean
);
create table if not exists foul_committed (
	event_id uuid references events(id),
	type varchar(30),
	penalty boolean,
    defensive boolean,
    card varchar(20),
    offensive boolean
);
create table if not exists goalkeeper (
	event_id uuid references events(id),
	outcome varchar(30),
	technique varchar(30),
	position varchar(20),
	body_part varchar(30),
	type varchar(30),
	end_location_x int,
	end_location_y int,
	shot_saved_to_post boolean,
	punched_out boolean,
	success_in_play boolean,
	shot_saved_off_target boolean,
	lost_out boolean,
	lost_in_play boolean
);
create table if not exists bad_behaviour (
	event_id uuid references events(id),
	card varchar(20)
);
-- create table if not exists own_goal_for (  NO FIELDS
-- 	event_id uuid references events(id),
-- );
-- create table if not exists player_on (  NO FIELDS
-- 	event_id uuid references events(id),
-- );
-- create table if not exists player_off (  NO FIELDS
-- 	event_id uuid references events(id),
-- );
-- create table if not exists shield (  NO FIELDS
-- 	event_id uuid references events(id),
-- );
-- create table if not exists camera_off ( TODO: what is this
-- 	event_id uuid references events(id),
-- );
create table if not exists pass (
	event_id uuid references events(id),
	recipient int references players(player_id),
	length real,
	angle real,
	height varchar(20),
	end_location_x real,
	end_location_y real,
	body_part varchar(20),
	type varchar(20),
	outcome varchar(20),
	aerial_won boolean,
	assisted_shot_id uuid references events(id),
	shot_assist boolean,
	switch boolean,
	"cross" boolean,
	deflected boolean,
	inswinging boolean,
	technique varchar(20),
	through_ball boolean,
	no_touch boolean,
	outswinging boolean,
	miscommunication boolean,
	cut_back boolean,
	goal_assist boolean,
	straight boolean
);
create table if not exists fifty_fifty (
	event_id uuid references events(id),
	outcome varchar(30)
);
-- create table if not exists half_end ( NO FIELDS
-- 	event_id uuid references events(id),
-- );
create table if not exists starting_xi (
	event_id uuid references events(id),
	formation int
	-- NOTE: event_tactics should also be linked
);
create table if not exists tactical_shift (
	event_id uuid references events(id),
	formation int
	-- NOTE: event_tactics should also be linked
);
-- create table if not exists error ( NO FIELDS
-- 	event_id uuid references events(id),
-- );
create table if not exists miscontrol (
	event_id uuid references events(id),
	aerial_won boolean
);
-- create table if not exists dribbled_past ( NO FIELDS
-- 	event_id uuid references events(id),
-- );
create table if not exists injury_stoppage (
	event_id uuid references events(id),
	in_chain boolean
);
-- create table if not exists referee_ball_drop ( NO FIELDS
-- 	event_id uuid references events(id),
-- );
create table if not exists ball_receipt (
	event_id uuid references events(id),
	outcome varchar(30)
);
create table if not exists carry (
	event_id uuid references events(id),
	end_location_x real,
	end_location_y real
);

-- Indices
create index matches_index
on matches(match_id);

create index competitions_index
on competitions(competition_id, season_id);

create index player_id_index
on players(player_id);

create index player_name_index
on players(player_name);

create index team_id_index
on teams(team_id);

create index team_name_index
on teams(team_name);

create index events_index 
on events(id);

