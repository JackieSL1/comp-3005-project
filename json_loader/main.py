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



def main():
    if not os.path.isdir(DATA_PATH):
        raise Exception(f"error: Couldn't find open-data at \"{DATA_PATH}\". Make sure it's been added to the project's root directory")


    with psycopg.connect(f"dbname={DATABASE} user={USERNAME} password={PASSWORD}") as conn:
        with conn.cursor() as cursor:
            cursor.execute("delete from competitions")
            competition_ids = set()
            competition_tuples = []
            season_tuples = []

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

            for competition in competition_tuples:
                cursor.execute("""
                            INSERT INTO competitions (
                                competition_id,
                                country_name,
                                competition_name,
                                competition_gender,
                                competition_youth,
                                competition_international
                            ) VALUES (%s, %s, %s, %s, %s, %s)
                        """, competition)

            for season in season_tuples:
                cursor.execute("""
                            INSERT INTO seasons (
                                season_id,
                                season_name,
                                competition_id
                            ) VALUES (%s, %s, %s)
                        """, season)


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
