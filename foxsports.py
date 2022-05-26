import re
from typing import Any, List
from requests import get

from scrape.date import Date
from scrape.scraper import Scraper
from scrape.parser import save_entry, assign_var

ROOT_URL = "https://api.foxsports.com"
LEAGUE = "MBL"
API_BASE_URL = "https://api.foxsports.com/bifrost/v1/mlb/league/scores-segment/"
CURRENT_API_KEY = "jE7yBJVRNAwdDesMgTzTXUUSx1It41Fq"
FOX_MLB_URL = "https://www.foxsports.com/mlb/scores"


class FoxSports:
    name: str = "Fox Sports"
    results: List[dict[str, Any]] = []

    def scrape(self) -> List:
        try:
            us_date = Date.get_US_date()
            target_url = f"{API_BASE_URL}{str(us_date)}?apikey={get_fox_api_key()}"
            print(target_url)

            match_data = self.handle_request(target_url)

            return self.follow_match_page(self.parse(match_data))

        except TypeError as e:
            return []

    def parse(self, data_response):
        results = []
        events = data_response["sectionList"][0]["events"]

        section_id = data_response["sectionList"][0]["id"]
        section_date = data_response["sectionList"][0]["sectionDate"]

        event_keys = {
            "mlbid": "id",
            "event_time": "eventTime",
            "status_line": "statusLine",
            "odds_line": "oddsLine",
            "over_underLine": "overUnderLine",
        }
        team_keys = {
            "complete_name": "imageAltText",
            "team_score": "score",
            "is_loser": "isLoser",
            "short_name": "name",
        }

        for event in events:
            row = {
                "source": self.name,
                "section_id": section_id,
                "section_date": section_date,
            }

            row.update(save_entry(event_keys, event, assign_var))
            row.update(save_entry(team_keys, event["upperTeam"], assign_var, "away_"))
            row.update(save_entry(team_keys, event["lowerTeam"], assign_var, "home_"))

            results.append(row)
        return results

    def follow_match_page(self, match_page_data: list) -> list:
        results = []

        total_keys = {
            "total": "betOutcomeLine",
        }
        spread_keys = {"spread": "text"}
        for row in match_page_data:
            mlbid = row["mlbid"].strip("mlb")
            if row["over_underLine"] != "_":
                game_url = f"https://api.foxsports.com/bifrost/v1/mlb/event/{mlbid}/matchup?apikey={CURRENT_API_KEY}"
                print(game_url)
                game_data = self.handle_request(game_url)
                odds_end = game_data["betSection"]["bets"][2]["model"]["odds"]

                row.update(
                    save_entry(
                        total_keys,
                        odds_end[0]["betSlip"]["trackingData"],
                        assign_var,
                        "home_",
                    )
                )

                row.update(
                    save_entry(
                        total_keys,
                        odds_end[1]["betSlip"]["trackingData"],
                        assign_var,
                        "away_",
                    )
                )

                row.update(save_entry(spread_keys, odds_end[0], assign_var, "home_"))
                row.update(save_entry(spread_keys, odds_end[1], assign_var, "away_"))

                results.append(row)
            else:
                continue
        return results
        # print(game_data)
        # for g in game_data:
        #     pass

    def handle_request(self, url) -> dict:
        r = get(url)

        if r.status_code != 200:
            print("\nOpps something went wrong")
            raise NotStatus200Error(f"{url}not 200 status, status is {r.status_code}")
        r.close()
        return r.json()


def get_fox_api_key():
    return CURRENT_API_KEY  # disable for now in development
    try:
        r = get(FOX_MLB_URL)
        apiKey = re.search(r"bifrost:\{apiKey:\"(.*?)\"", r.text).group(1)
        return apiKey if (apiKey) else CURRENT_API_KEY

    except Exception as e:
        print(e)
        print("Send message to email or discord . . . ")
        return CURRENT_API_KEY

    finally:
        r.close()


class NotStatus200Error(Exception):
    pass


def main():
    import json

    fox = FoxSports()
    with Scraper(fox, ROOT_URL, LEAGUE) as results:
        # for r in results:
        #     print(r)
        with open("data.json", "w") as f:
            json.dump(results, f)


if __name__ == "__main__":
    main()
