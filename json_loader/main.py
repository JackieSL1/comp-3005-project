import psycopg 
import json
import os
import time
from constants import (
    SEASONS,
    COLUMNS,
    DATABASE,
    USERNAME,
    PASSWORD,
    PORT,
    HOST,
    DATA_PATH,
    EVENT_JSON_KEYS,
    EVENT_JSON_TO_TABLE,
)

def insert(cursor, table, tuples):
    columns = COLUMNS[table]

    for record in tuples:
        try:
            cursor.execute(f"""
                            INSERT INTO {table} ({', '.join(columns)})
                            VALUES ({', '.join(['%s'] * len(columns))})
                            """, record)
        except Exception as e:
            print(f"""
                   INSERT INTO {table} ({', '.join(columns)})
                   VALUES ({', '.join(['%s'] * len(columns))})
                   """)
            print(record)
            print(e)
            breakpoint()
            raise e

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
    competition_tuples = []

    print("Building competitions")
    with open(f"{DATA_PATH}competitions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for competition in data:

            # Skip data related to other seasons
            if (competition['competition_name'], competition['season_name']) not in SEASONS:
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

            competition_ids.add((competition['competition_id'], competition['season_id']))

    print("Done")

    # Build list of json files with matches data
    matches_paths = []
    for competition, match in competition_ids:
        matches_paths.append(f"{DATA_PATH}matches/{competition}/{match}.json")

    print(matches_paths)

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
    related_events = []
    event_tactics = []

    print("Building events")
    for path in events_paths:
        with open(path, "r", encoding = "utf-8") as f:
            data = json.load(f)

            for event in data:
                match_id = path.split("/")[-1].split(".")[0]

                event_types.append((
                    event["type"]["id"],
                    EVENT_JSON_TO_TABLE[event["type"]["name"]],
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

                if event.get("related_events"):
                    for related_event_id in event["related_events"]:
                        related_events.append((
                            event["id"],
                            related_event_id, 
                        ))


                event_name = event["type"]["name"]
                value = event.get(EVENT_JSON_TO_TABLE[event_name])

                match event_name:
                    case "Ball Recovery":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                               event["id"],
                               value.get("recovery_failure"), 
                               value.get("offensive"), 
                            ))
                    case "Dispossessed":
                            # No extra fields
                            pass
                    case "Duel":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                               event["id"],
                               value.get("type", {}).get("name"), 
                               value.get("outcome", {}).get("name"), 
                            ))
                    case "Camera On":
                        # TODO: Is this even an event?
                        pass
                    case "Block":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("deflection"),
                                value.get("offensive"),
                                value.get("save_block"),
                            ))
                    case "Offside":
                            # no fields
                        pass
                    case "Clearance":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("body_part", {}).get("name"),
                            ))
                    case "Interception":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("outcome", {}).get("name"),
                            ))
                    case "Dribble":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("outcome", {}).get("name"),
                                value.get("overrun"),
                                value.get("nutmeg"),
                                value.get("no_touch"),
                            ))
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
                            shot.get("type", {}).get("name"),
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
                        # no fields
                        pass
                    case "Half Start":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("late_video_start"),
                            ))
                    case "Substitution":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("outcome", {}).get("name"), 
                                value.get("replacement", {}).get("id"),
                            ))
                    case "Own Goal Against":
                        # no fields
                        pass
                    case "Foul Won":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("penalty"),
                                value.get("defensive"),
                                value.get("advantage"),
                            ))
                    case "Foul Committed":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("type", {}).get("name"),
                                value.get("penalty"),
                                value.get("defensive"),
                                value.get("card", {}).get("name"),
                                value.get("offensive"),
                            ))
                    case "Goal Keeper":
                        if value:
                            location_x, location_y = value.get("end_location", (None, None))
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("outcome", {}).get("name"),
                                value.get("technique", {}).get("name"),
                                value.get("position", {}).get("name"),
                                value.get("body_part", {}).get("name"),
                                value.get("type", {}).get("name"),
                                location_x,
                                location_y,
                                value.get("shot_saved_to_post"),
                                value.get("punched_out"),
                                value.get("success_in_play"),
                                value.get("shot_saved_off_target"),
                                value.get("lost_out"),
                                value.get("lost_in_play"),
                            ))
                    case "Bad Behaviour":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("card", {}).get("name"),
                            ))
                    case "Own Goal For":
                        # no fields
                        pass
                    case "Player On":
                        # no fields
                        pass
                    case "Player Off":
                        # no fields
                        pass
                    case "Shield":
                        # no fields
                        pass
                    case "Camera off":
                        # TODO: Is this even an event?
                        pass
                    case "Pass":
                        if value:
                            location_x, location_y = value.get("end_location", (None, None))
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("recipient", {}).get("id"),
                                value.get("length"),
                                value.get("angle"),
                                value.get("height", {}).get("name"),
                                location_x,
                                location_y,
                                value.get("body_part", {}).get("name"),
                                value.get("type", {}).get("name"),
                                value.get("outcome", {}).get("name"),
                                value.get("aerial_won"),
                                value.get("assisted_shot_id"),
                                value.get("shot_assist"),
                                value.get("switch"),
                                value.get("cross"),
                                value.get("deflected"),
                                value.get("inswinging"),
                                value.get("technique", {}).get("name"),
                                value.get("through_ball"),
                                value.get("no_touch"),
                                value.get("outswinging"),
                                value.get("miscommunication"),
                                value.get("cut_back"),
                                value.get("goal_assist"),
                                value.get("straight"),
                            ))
                    case "50/50":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("outcome", {}).get("name"),
                            ))
                    case "Half End":
                        # no fields
                        pass
                    case "Starting XI":
                        value = event.get("tactics")
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("formation"),
                            ))

                            for player in value.get("lineup"):
                                event_tactics.append((
                                    event["id"],
                                    player["player"]["id"],
                                    player["position"]["id"],
                                    player["jersey_number"],
                                ))
                    case "Tactical Shift":
                        value = event.get("tactics")
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("formation"),
                            ))

                            for player in value.get("lineup"):
                                event_tactics.append((
                                    event["id"],
                                    player["player"]["id"],
                                    player["position"]["id"],
                                    player["jersey_number"],
                                ))
                    case "Error":
                        pass
                    case "Miscontrol":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("aerial_won"),
                            ))
                    case "Dribbled Past":
                        pass
                    case "Injury Stoppage":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("in_chain"),
                            ))
                    case "Referee Ball-Drop":
                        pass
                    case "Ball Receipt*":
                        if value:
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                value.get("outcome", {}).get("name"),
                            ))
                    case "Carry":
                        if value:
                            location_x, location_y = value.get("end_location", (None, None))
                            event_tuples[EVENT_JSON_TO_TABLE[event_name]].append((
                                event["id"],
                                location_x,
                                location_y,
                            ))
                    case _:
                        raise Exception("error: Event type " + event["type"]["name"] + " not recognized")

    print("Done")

    print("Inserting into database")

    # Insert all data
    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={PASSWORD} host={HOST} port={PORT}") as conn:
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
            insert(cursor, "event_tactics", event_tactics)
            insert(cursor, "related_events", related_events)

            for event_key in EVENT_JSON_KEYS.keys():
                insert(cursor, event_key, event_tuples[event_key])



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
