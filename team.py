import time
import pandas
import requests
from io import StringIO
from pathlib import Path
from bs4 import BeautifulSoup


class Team:
    all_players = []

    html = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table', class_='stats_table')[0]

    links = table.find_all('a')
    links = [l.get('href') for l in links]
    links = [l for l in links if '/squads/' in l]

    team_urls = [f'https://fbref.com{l}' for l in links]

    for team_url in team_urls:
        team_name = team_url.split('/')[-1].replace('-Stats', '')
        data = requests.get(team_url).text
        soup = BeautifulSoup(data, 'lxml')
        stats = soup.find_all('table', class_='stats_table')[0]

        if stats and stats.columns:
            stats.columns = stats.columns.droplevel()

        team_data = pandas.read_html(StringIO(str(stats)))[0]
        team_data["Team"] = team_name
        all_players.append(team_data)
        time.sleep(3)

        stat_df = pandas.concat(all_players)
        filepath = Path(('league-data/teams-players/' + team_name + '.csv'))
        filepath.parent.mkdir(parents=True, exist_ok=True)
        stat_df.to_csv(filepath)
        all_players.clear()
