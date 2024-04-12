DATABASE: str = "project_database"
USERNAME: str = "postgres"
PASSWORD: str = "1234"
HOST: str = "localhost"
PORT: str = "5432"
DATA_PATH: str = "./open-data/data/"
SEASONS: list[tuple[str, str]] = [
    ('La Liga', "2020/2021"),
    ('La Liga', "2019/2020"),
    ('La Liga', "2018/2019"),
    ('Premier League', "2003/2004"),
]

# NOTE: When adding a new table, add its columns here
COLUMNS = {
    "competitions": (
        "competition_id",
        "season_id",
        "season_name",
        "country_name",
        "competition_name",
        "competition_gender",
        "competition_youth",
        "competition_international",
    ),
    "countries": (
        "country_id",
        "name",
    ),
    "managers": (
        "manager_id",
        "name",
        "nickname",
        "dob",
        "country_id",
    ),
    "team_managers": (
        "team_id",
        "manager_id",
    ),
    "competition_stages": (
        "competition_stage_id",
        "name",
    ),
    "stadiums": (
        "stadium_id",
        "name",
        "country_id",
    ),
    "referees": (
        "referee_id",
        "name",
        "country_id",
    ),
    "matches": (
        "match_id",
        "match_date",
        "kick_off",
        "competition_id",
        "season_id",
        "home_team_id",
        "away_team_id",
        "home_score",
        "away_score",
        "match_week",
        "competition_stage_id",
        "stadium_id",
        "referee_id",
    ),
    "teams": (
        "team_id",
        "team_name",
        "team_gender",
        "team_group",
        "country_id",
    ),
    "lineups": (
        "match_id",
        "team_id",
        "player_id",
        "jersey_number",
    ),
    "players": (
        "player_id",
        "player_name",
        "player_nickname",
        "country",
    ),
    "cards": (
        "player_id",
        "match_id",
        "time",
        "card_type",
        "reason",
        "period",
    ),
    "positions": (
        "position_id",
        "position",
    ),
    "player_positions": (
        "player_id",
        "match_id",
        "position_id",
        "\"from\"",
        "\"to\"",
        "from_period",
        "to_period",
        "start_reason",
        "end_reason",
    ),
    "event_types": (
        "event_type_id",
        "name",
    ),
    "events": (
        "id",
        "match_id",
        "index",
        "period",
        "timestamp",
        "minute",
        "second",
        "event_type_id",
        "posession",
        "posession_team_id",
        "play_pattern",
        "team_id",
        "player_id",
        "position",
        "location_x",
        "location_y",
        "duration",
        "under_pressure",
        "counterpress",
        "out",
    ),
    "event_tactics": (
        "event_id",
        "player_id",
        "position",
        "jersey_number",
    ),
    "related_events": (
        "event_id",
        "related_event_id",
    ),
    "shot": (
        "event_id",
        "statsbomb_xg",
        "end_location_x",
        "end_location_y",
        "end_location_z",
        "key_pass_id",
        "body_part",
        "type",
        "outcome",
        "first_time",
        "technique",
        "deflected",
        "one_on_one",
        "aerial_won",
        "saved_to_post",
        "redirect",
        "open_goal",
        "follows_dribble",
        "saved_off_target",
    ),
    "ball_recovery": (
        "event_id",
        "recovery_failure",
        "offensive",
    ),
    "dispossessed": (

    ),
    "duel": (
        "event_id",
        "type",
        "outcome",
    ),
    "camera_on": (
        # TODO: Is this even an event?
    ),
    "block": (
        "event_id",
        "deflection",
        "offensive",
        "save_block",
    ),
    "offside": (
        # no fields
    ),
    "clearance": (
        "event_id",
        "body_part"
    ),
    "interception": (
        "event_id",
        "outcome"
    ),
    "dribble": (
        "event_id",
        "outcome",
        "overrun",
        "nutmeg",
        "no_touch",
    ),
    "pressure": (
        # no fields
    ),
    "half_start": (
        "event_id",
        "late_video_start",
    ),
    "substitution": (
        "event_id",
        "outcome",
        "replacement",
    ),
    "own_goal_against": (
        # no fields
    ),
    "foul_won": (
        "event_id",
        "penalty",
        "defensive",
        "advantage",
    ),
    "foul_committed": (
        "event_id",
        "type",
        "penalty",
        "defensive",
        "card",
        "offensive",
    ),
    "goalkeeper": (
        "event_id",
        "outcome",
        "technique",
        "position",
        "body_part",
        "type",
        "end_location_x",
        "end_location_y",
        "shot_saved_to_post",
        "punched_out",
        "success_in_play",
        "shot_saved_off_target",
        "lost_out",
        "lost_in_play",
    ),
    "bad_behaviour": (
        "event_id",
        "card",
    ),
    "own_goal_for": (
        # no fields
    ),
    "player_on": (
        # no fields
    ),
    "player_off": (
        # no fields
    ),
    "shield": (
        # no fields
    ),
    "camera_off": (
        # TODO: Is this even an event?
    ),
    "pass": (
        "event_id",
        "recipient",
        "length",
        "angle",
        "height",
        "end_location_x",
        "end_location_y",
        "body_part",
        "type",
        "outcome",
        "aerial_won",
        "assisted_shot_id",
        "shot_assist",
        "switch",
        "\"cross\"",
        "deflected",
        "inswinging",
        "technique",
        "through_ball",
        "no_touch",
        "outswinging",
        "miscommunication",
        "cut_back",
        "goal_assist",
        "straight",
    ),
    "fifty_fifty": (
        "event_id",
        "outcome",
    ),
    "half_end": (
        # no fields
    ),
    "starting_xi": (
        "event_id",
        "formation",
    ),
    "tactical_shift": (
        "event_id",
        "formation",
    ),
    "error": (
        # no fields
    ),
    "miscontrol": (
        "event_id",
        "aerial_won",
    ),
    "dribbled_past": (
        # no fields
    ),
    "injury_stoppage": (
        "event_id",
        "in_chain",
    ),
    "referee_ball_drop": (
        # no fields
    ),
    "ball_receipt": (
        "event_id",
        "outcome",
    ),
    "carry": (
        "event_id",
        "end_location_x",
        "end_location_y",
    ),
}

# Each key corresponds to an event type in the JSON data
# The values are a list of JSON keys to get the correct values from the data
EVENT_JSON_KEYS = {
    "ball_recovery": (

    ),
    "dispossessed": (

    ),
    "duel": (

    ),
    "camera_on": (

    ),
    "block": (

    ),
    "offside": (

    ),
    "clearance": (

    ),
    "interception": (

    ),
    "dribble": (

    ),
    "shot": (
        "event_id",
        "statsbomb_xg",
        "end_location",
        "end_location",
        "end_location",
        "key_pass_id",
        "body_part",
        ("type", "id"),
        "outcome",
        "first_time",
        "technique",
        "deflected",
        "one_on_one",
        "aerial_won",
        "saved_to_post",
        "redirect",
        "open_goal",
        "follows_dribble",
        "saved_off_target",
    ),
    "pressure": (

    ),
    "half_start": (

    ),
    "substitution": (

    ),
    "own_goal_against": (

    ),
    "foul_won": (

    ),
    "foul_committed": (

    ),
    "goalkeeper": (

    ),
    "bad_behaviour": (

    ),
    "own_goal_for": (

    ),
    "player_on": (

    ),
    "player_off": (

    ),
    "shield": (

    ),
    "camera_off": (

    ),
    "pass": (

    ),
    "fifty_fifty": (

    ),
    "half_end": (

    ),
    "starting_xi": (

    ),
    "tactical_shift": (

    ),
    "error": (

    ),
    "miscontrol": (

    ),
    "dribbled_past": (

    ),
    "injury_stoppage": (

    ),
    "referee_ball_drop": (

    ),
    "ball_receipt": (

    ),
    "carry": (

    ),
}

EVENT_JSON_TO_TABLE = {
    "Ball Recovery"    : "ball_recovery",
    "Dispossessed"     : "dispossessed",
    "Duel"             : "duel",
    "Camera On"        : "camera_on",
    "Block"            : "block",
    "Offside"          : "offside",
    "Clearance"        : "clearance",
    "Interception"     : "interception",
    "Dribble"          : "dribble",
    "Shot"             : "shot",
    "Pressure"         : "pressure",
    "Half Start"       : "half_start",
    "Substitution"     : "substitution",
    "Own Goal Against" : "own_goal_against",
    "Foul Won"         : "foul_won",
    "Foul Committed"   : "foul_committed",
    "Goal Keeper"      : "goalkeeper",
    "Bad Behaviour"    : "bad_behaviour",
    "Own Goal For"     : "own_goal_for",
    "Player On"        : "player_on",
    "Player Off"       : "player_off",
    "Shield"           : "shield",
    "Camera off"       : "camera_off",
    "Pass"             : "pass",
    "50/50"            : "fifty_fifty",
    "Half End"         : "half_end",
    "Starting XI"      : "starting_xi",
    "Tactical Shift"   : "tactical_shift",
    "Error"            : "error",
    "Miscontrol"       : "miscontrol",
    "Dribbled Past"    : "dribbled_past",
    "Injury Stoppage"  : "injury_stoppage",
    "Referee Ball-Drop": "referee_ball_drop",
    "Ball Receipt*"    : "ball_receipt",
    "Carry"            : "carry",
}
