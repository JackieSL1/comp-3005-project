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
        "country_name",
        "competition_name",
        "competition_gender",
        "competition_youth",
        "competition_international",
    ),
    "seasons": (
        "season_id",
        "season_name",
        "competition_id",
    )
}

# TODO: Delete before submission
""" SCRATCH PAD
Tables:
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



def main():
    if not os.path.isdir(DATA_PATH):
        raise Exception(f"error: Couldn't find open-data at \"{DATA_PATH}\". Make sure it's been added to the project's root directory")


    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={PASSWORD}") as conn:
        with conn.cursor() as cursor:
            competition_ids = set()
            competition_tuples = []
            season_tuples = []

            # TODO: This shouldn't be run everytime - remove when script is done
            with open("./ddl.sql", 'r') as ddl:
                cursor.execute(ddl.read()) # type: ignore

            with open(f"{DATA_PATH}competitions.json", "r") as f:
                data = json.load(f)
                for row in data:

                    # Skip data related to other seasons
                    if row['season_name'] not in SEASONS:
                        continue

                    if row['competition_id'] not in competition_ids:
                        competition_tuples.append((
                            row['competition_id'],
                            row['country_name'],
                            row['competition_name'],
                            row['competition_gender'],
                            row['competition_youth'],
                            row['competition_international'],
                        ))

                        competition_ids.add(row['competition_id'])

                    season_tuples.append((
                        row['season_id'],
                        row['season_name'],
                        row['competition_id'],
                    ))

            insert(cursor, "competitions",  competition_tuples)
            insert(cursor, "seasons",  season_tuples)


            # Build list of json files with matches data
            # matches_paths = []
            # for id in competition_ids:
            #     with os.scandir(f"{DATA_PATH}matches/{id}") as dirs:
            #         for path in dirs:
            #             matches_paths.append(path.path)
            #
            #
            # for path in matches_paths:
            #     with open(path, "r") as f:
            #         data = json.load(f)
            #         for match in data:



if __name__ == "__main__":
    main()
