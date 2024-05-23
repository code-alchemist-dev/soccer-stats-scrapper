import re
import time
import pandas
import requests
from io import StringIO
from pathlib import Path
from bs4 import BeautifulSoup


class League:
    leagues = []
    links = [
        '9/Premier-League-Stats',
        '52/Premier-Division-Stats',
        '12/La-Liga-Stats',
        '11/Serie-A-Stats',
        '20/Bundesliga-Stats',
        '13/Ligue-1-Stats'
    ]

    for link in links:

        html = requests.get(f'https://fbref.com/en/comps/{link}').text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all('table', class_='stats_table')[0]

        if table and table.columns:
            table.columns = table.columns.droplevel()

        team_data = pandas.read_html(StringIO(str(table)))[0]
        leagues.append(team_data)

        stat_df = pandas.concat(leagues)
        filepath = Path(('league-data/team-tables/' + re.sub(r'^.*?/', '', link) + '.csv'))
        filepath.parent.mkdir(parents=True, exist_ok=True)
        stat_df.to_csv(filepath)
        time.sleep(5)
        leagues.clear()
