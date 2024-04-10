DATABASE: str = "testing"
USERNAME: str = "postgres"
PASSWORD: str = "postgres"
DATA_PATH: str = "./open-data/data/"
SEASONS: list[str] = [
    "2020/2021",
    "2019/2020",
    "2018/2019",
    "2003/2004",
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
    "goal_keeper": (

    ),
    "bad_behaviour": (

    ),
    "own goal_for": (

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
    "50_50": (

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
        "match_id",
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
    "goal_keeper": (

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
    "50_50": (

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
    "referee_ball-drop": (

    ),
    "ball_receipt": (

    ),
    "carry": (

    ),
}
