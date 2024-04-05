import psycopg
import json
import os

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

# TODO: Could move this to a separate config file for easier modification 
# (doesn't really matter though)

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
    # "seasons": (
    # ),
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
}

# TODO: Delete before submission
""" SCRATCH PAD
Tables:
competitions
seasons
countries
managers
competition_stages
stadiums
referees
matches
teams
team_managers
position
players
"""

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

def main():
    if not os.path.isdir(DATA_PATH):
        raise Exception(f"error: Couldn't find open-data at \"{DATA_PATH}\". Make sure it's been added to the project's root directory")


    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={PASSWORD}") as conn:
        with conn.cursor() as cursor:
            competition_ids = set()
            season_ids = set()
            competition_tuples = []
            # season_tuples = []

            # TODO: This shouldn't be run everytime - remove when script is done
            with open("./ddl.sql", 'r') as ddl:
                cursor.execute(ddl.read()) # type: ignore

            with open(f"{DATA_PATH}competitions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for row in data:

                    # Skip data related to other seasons
                    if row['season_name'] not in SEASONS:
                        continue

                    competition_tuples.append((
                        row['competition_id'],
                        row['season_id'],
                        row['season_name'],
                        row['country_name'],
                        row['competition_name'],
                        row['competition_gender'],
                        row['competition_youth'],
                        row['competition_international'],
                    ))

                    competition_ids.add(row['competition_id'])
                    season_ids.add(row['season_id'])

                    # season_tuples.append((
                    #     row['season_id'],
                    #     row['season_name'],
                    #     row['competition_id'],
                    # ))

            insert(cursor, "competitions",  competition_tuples)
            # insert(cursor, "seasons",  season_tuples) 

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

            for path in matches_paths:
                with open(path, "r", encoding = "utf-8") as f:
                    data = json.load(f)

                    for match in data:
                        for country in (match["home_team"]["country"],
                                        match["away_team"]["country"],
                                        ):
                            country_tuples.append((
                                country["id"],
                                country["name"],
                            ))

                        referee = match.get("referee", None)
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

                        stadium = match.get("stadium", None)
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

            insert(cursor, "countries",  remove_duplicates_from_tuples(country_tuples))
            insert(cursor, "competition_stages",  remove_duplicates_from_tuples(competition_stage_tuples))
            insert(cursor, "stadiums",  remove_duplicates_from_tuples(stadium_tuples))
            insert(cursor, "referees",  remove_duplicates_from_tuples(referee_tuples))
            insert(cursor, "teams",  remove_duplicates_from_tuples(team_tuples))
            insert(cursor, "managers",  remove_duplicates_from_tuples(manager_tuples))
            insert(cursor, "team_managers",  remove_duplicates_from_tuples(team_manager_tuples))
            insert(cursor, "matches",  remove_duplicates_from_tuples(match_tuples))









if __name__ == "__main__":
    main()
