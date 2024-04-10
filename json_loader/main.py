import psycopg 
import json
import os
import time
from constants import (
    SEASONS, # TODO: Make sure this includes all seasons
    COLUMNS,
    DATABASE,
    USERNAME,
    PASSWORD,
    DATA_PATH,
    EVENT_JSON_KEYS,
)

def insert(cursor, table, tuples):
    columns = COLUMNS[table]

    for record in tuples:
        cursor.execute(f"""
                        INSERT INTO {table} ({', '.join(columns)})
                        VALUES ({', '.join(['%s'] * len(columns))})
                        """, record)

def remove_duplicates_from_tuples(tuples: list[tuple]):
    seen_ids = set()
    def unique(tup: tuple) -> bool:
        if tup[0] in seen_ids:
            return False

        seen_ids.add(tup[0])
        return True

    return filter(unique, tuples)

def build_list_from_json(json: dict, keys: list) -> list:
    result = []

    for key in keys:
        if type(key) == str:
            # If key is a single string, extract that value
            result.append(json.get(key))
        else:
            # Otherwise the key should be a list of keys - iterate to find nested value
            value = json
            for nested_key in key:
                value = value.get(nested_key)
                if value is None:
                    break

            result.append(value)

    return list(result)




def main():
    if not os.path.isdir(DATA_PATH):
        raise Exception(f"error: Couldn't find open-data at \"{DATA_PATH}\". Make sure it's been added to the project's root directory")


    competition_ids = set()
    season_ids = set()
    competition_tuples = []

    # TODO: This shouldn't be run everytime - remove when script is done
    # with open("./ddl.sql", 'r') as ddl:
    #     cursor.execute(ddl.read()) # type: ignore

    print("Building competitions")
    with open(f"{DATA_PATH}competitions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for competition in data:

            # Skip data related to other seasons
            if competition['season_name'] not in SEASONS:
                continue

            competition_tuples.append(build_list_from_json(competition, (
                'competition_id',
                'season_id',
                'season_name',
                'country_name',
                'competition_name',
                'competition_gender',
                'competition_youth',
                'competition_international',
            )))

            competition_ids.add(competition['competition_id'])
            season_ids.add(competition['season_id'])

    print("Done")

    # Build list of json files with matches data
    matches_paths = []
    for id in competition_ids:
        with os.scandir(f"{DATA_PATH}matches/{id}") as dirs:
            for path in dirs:
                if int(path.name.split(".")[0]) in season_ids:
                    matches_paths.append(path.path)

    country_tuples = []
    manager_tuples = []
    competition_stage_tuples = []
    stadium_tuples = []
    referee_tuples = []
    match_tuples = []
    team_tuples = []
    team_manager_tuples = []
    
    # Used to find lineups
    match_ids = set()

    print("Building matches")
    for path in matches_paths:
        with open(path, "r", encoding = "utf-8") as f:
            data = json.load(f)

            for match in data:
                match_ids.add(match["match_id"])

                for country in (match["home_team"]["country"],
                                match["away_team"]["country"],
                                ):
                    country_tuples.append((
                        country["id"],
                        country["name"],
                    ))

                referee = match.get("referee")
                if referee is not None:
                    country_tuples.append((
                        referee["country"]["id"],
                        referee["country"]["name"],
                    ))
                    referee_tuples.append((
                        match["referee"]["id"],
                        match["referee"]["name"],
                        match["referee"]["country"]["id"],
                    ))
                    referee = referee["id"]

                stadium = match.get("stadium")
                if stadium is not None:
                    country_tuples.append((
                        stadium["country"]["id"],
                        stadium["country"]["name"],
                    ))
                    stadium_tuples.append((
                        stadium["id"],
                        stadium["name"],
                        stadium["country"]["id"],
                    ))
                    stadium = stadium["id"]

                for manager in match["home_team"].get("managers", ()):
                    manager_tuples.append((
                        manager["id"],
                        manager["name"],
                        manager["nickname"],
                        manager["dob"],
                        manager["country"]["id"],
                    ))
                    country_tuples.append((
                        manager["country"]["id"],
                        manager["country"]["name"],
                    ))
                    team_manager_tuples.append((
                        match["home_team"]["home_team_id"],
                        manager["id"],
                    ))

                for manager in match["away_team"].get("managers", ()):
                    manager_tuples.append((
                        manager["id"],
                        manager["name"],
                        manager["nickname"],
                        manager["dob"],
                        manager["country"]["id"],
                    ))
                    country_tuples.append((
                        manager["country"]["id"],
                        manager["country"]["name"],
                    ))
                    team_manager_tuples.append((
                        match["away_team"]["away_team_id"],
                        manager["id"],
                    ))

                competition_stage_tuples.append((
                    match["competition_stage"]["id"],
                    match["competition_stage"]["name"],
                ))

                team_tuples.append((
                    match["home_team"]["home_team_id"],
                    match["home_team"]["home_team_name"],
                    match["home_team"]["home_team_gender"],
                    match["home_team"]["home_team_group"],
                    match["home_team"]["country"]["id"],
                ))

                team_tuples.append((
                    match["away_team"]["away_team_id"],
                    match["away_team"]["away_team_name"],
                    match["away_team"]["away_team_gender"],
                    match["away_team"]["away_team_group"],
                    match["away_team"]["country"]["id"],
                ))

                match_tuples.append((
                    match["match_id"],
                    match["match_date"],
                    match["kick_off"],
                    match["competition"]["competition_id"],
                    match["season"]["season_id"],
                    match["home_team"]["home_team_id"],
                    match["away_team"]["away_team_id"],
                    match["home_score"],
                    match["away_score"],
                    match["match_week"],
                    match["competition_stage"]["id"],
                    stadium,
                    referee,
                ))

    print("Done")

    # Build list of json files with lineups data
    lineups_paths = []
    for id in match_ids:
        lineups_paths.append(f"{DATA_PATH}lineups/{id}.json")

    lineup_tuples = []
    player_tuples = []
    card_tuples = []
    position_tuples = []
    player_position_tuples = []

    print("Building lineups")
    for path in lineups_paths:
        with open(path, "r", encoding = "utf-8") as f:
            data = json.load(f)

            for lineup in data:
                match_id = path.split("/")[-1].split(".")[0]
                for player in lineup["lineup"]:

                    player_tuples.append((
                        player["player_id"],
                        player["player_name"],
                        player["player_nickname"],
                        player["country"]["id"],
                    ))

                    lineup_tuples.append((
                        match_id,
                        lineup["team_id"],
                        player["player_id"],
                        player["jersey_number"],
                    ))

                    country_tuples.append((
                        player["country"]["id"],
                        player["country"]["name"],
                    ))

                    for card in player["cards"]:
                        card_tuples.append((
                            player["player_id"],
                            match_id,
                            card["time"],
                            card["card_type"],
                            card["reason"],
                            card["period"],
                        ))

                    for position in player["positions"]:
                        position_tuples.append((
                            position["position_id"], 
                            position["position"],
                        ))

                        player_position_tuples.append((
                            player["player_id"],
                            match_id,
                            position["position_id"], 
                            position["from"],
                            position["to"],
                            position["from_period"],
                            position["to_period"],
                            position["start_reason"],
                            position["end_reason"],
                        ))

    # Build list of json files with events data
    events_paths = []
    for id in match_ids:
        events_paths.append(f"{DATA_PATH}events/{id}.json")

    events = []
    event_types = []
    event_tuples = {key : list() for key in EVENT_JSON_KEYS}

    print("Building events")
    for path in events_paths:
        with open(path, "r", encoding = "utf-8") as f:
            data = json.load(f)

            for event in data:
                match_id = path.split("/")[-1].split(".")[0]

                event_types.append((
                    event["type"]["id"],
                    event["type"]["name"],
                ))

                if event.get("position"):
                    position_tuples.append((
                        event["position"]["id"],
                        event["position"]["name"],
                    ))

                if event.get("location"):
                    location_x, location_y = event.get("location")
                else:
                    location_x, location_y = None, None

                events.append((
                    event["id"],
                    match_id,
                    event["index"],
                    event["period"],
                    event["timestamp"],
                    event["minute"],
                    event["second"],
                    event["type"]["id"],
                    event.get("possession"),
                    event.get("possession_team", {}).get("id"),
                    event.get("play_pattern", {}).get("name"),
                    event.get("team", {}).get("id"),
                    event.get("player", {}).get("id"),
                    event.get("position", {}).get("id"),
                    location_x,
                    location_y,
                    event.get("duriation"),
                    event.get("under_pressure"),
                    event.get("counterpress"),
                    event.get("out"),
                ))

                match event["type"]["name"]:
                    case "Ball Recovery":
                        pass
                    case "Dispossessed":
                        pass
                    case "Duel":
                        pass
                    case "Camera On":
                        pass
                    case "Block":
                        pass
                    case "Offside":
                        pass
                    case "Clearance":
                        pass
                    case "Interception":
                        pass
                    case "Dribble":
                        pass
                    case "Shot":
                        shot = event["shot"]
                        location = shot.get("location")
                        location_z = None

                        if location:
                            if len(location == 2):
                                location_x, location_y = location
                            if len(location == 3):
                                location_x, location_y, location_z = location

                        event_tuples["shot"].append((
                            event["id"],
                            shot["statsbomb_xg"],
                            location_x,
                            location_y,
                            location_z,
                            shot.get("key_pass_id"),
                            shot.get("body_part", {}).get("name"),
                            shot["type"]["id"],
                            shot.get("outcome", {}).get("name"),
                            shot.get("first_time"),
                            shot.get("technique", {}).get("name"),
                            shot.get("deflected"),
                            shot.get("one_on_one"),
                            shot.get("aerial_won"),
                            shot.get("saved_to_post"),
                            shot.get("redirect"),
                            shot.get("open_goal"),
                            shot.get("follows_dribble"),
                            shot.get("saved_off_target"),
                        ))
                    case "Pressure":
                        pass
                    case "Half Start":
                        pass
                    case "Substitution":
                        pass
                    case "Own Goal Against":
                        pass
                    case "Foul Won":
                        pass
                    case "Foul Committed":
                        pass
                    case "Goal Keeper":
                        pass
                    case "Bad Behaviour":
                        pass
                    case "Own Goal For":
                        pass
                    case "Player On":
                        pass
                    case "Player Off":
                        pass
                    case "Shield":
                        pass
                    case "Camera off":
                        pass
                    case "Pass":
                        pass
                    case "50/50":
                        pass
                    case "Half End":
                        pass
                    case "Starting XI":
                        pass
                    case "Tactical Shift":
                        pass
                    case "Error":
                        pass
                    case "Miscontrol":
                        pass
                    case "Dribbled Past":
                        pass
                    case "Injury Stoppage":
                        pass
                    case "Referee Ball-Drop":
                        pass
                    case "Ball Receipt*":
                        pass
                    case "Carry":
                        pass
                    case _:
                        raise Exception("error: Event type " + event["type"]["name"] + " not recognized")

    print("Done")

    print("Inserting into database")

    # Insert all data
    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={PASSWORD}") as conn:
        with conn.cursor() as cursor:

            insert(cursor, "competitions",  competition_tuples)
            insert(cursor, "countries",  remove_duplicates_from_tuples(country_tuples))
            insert(cursor, "competition_stages",  remove_duplicates_from_tuples(competition_stage_tuples))
            insert(cursor, "stadiums",  remove_duplicates_from_tuples(stadium_tuples))
            insert(cursor, "referees",  remove_duplicates_from_tuples(referee_tuples))
            insert(cursor, "teams",  remove_duplicates_from_tuples(team_tuples))
            insert(cursor, "managers",  remove_duplicates_from_tuples(manager_tuples))
            insert(cursor, "team_managers",  remove_duplicates_from_tuples(team_manager_tuples))
            insert(cursor, "matches",  remove_duplicates_from_tuples(match_tuples))
            insert(cursor, "players",  remove_duplicates_from_tuples(player_tuples))
            insert(cursor, "lineups",  lineup_tuples)
            insert(cursor, "cards",  card_tuples)
            insert(cursor, "positions",  remove_duplicates_from_tuples(position_tuples))
            insert(cursor, "player_positions", remove_duplicates_from_tuples(player_position_tuples))
            insert(cursor, "event_types", remove_duplicates_from_tuples(event_types))
            insert(cursor, "events", events)

            # for event_key in EVENT_JSON_KEYS.keys():
            #     insert(cursor, event_key, event_tuples[event_key])

            insert(cursor, "shot", event_tuples["shot"])


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
