import requests

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def league_table():
    # page link of the site were data will be extracted
    url = 'https://www.bbc.com/sport/football/premier-league/table'
    # list to store the headers
    headers = []
    # makes a get request that returns the html
    page = requests.get(url)

    # used to clean and sort throught the html content to get the needed data
    soup = BeautifulSoup(page.text, 'html.parser')
    # find the content in this html tag, using class_ cause class is a key world
    table = soup.find('ta', class_='ssrcss-14j0ip6-Table e3bga5w5')

    # finds all html tags with th header
    for th in table.find_all('th'): 
        # gets the text content
        title = th.text
        # appends the title to the headers
        headers.append(title)

    #creates dataframes with the headers
    league_table = pd.DataFrame(columns=headers)

    # finds all the html tags with tr
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [td.text.strip() for td in row_data]
        lenght = len(league_table)
        # gets them by row and saves to the league table dataframe
        league_table.loc[lenght] = row

    league_table.drop('Form, last 6 games, oldest first', axis=1, inplace=True)

    return league_table

def top_scorers():
    # page link of the site were data will be extracted
    url = 'https://www.bbc.com/sport/football/premier-league/top-scorers'
    # list to store the headers
    headers = []
    # makes a get request that returns the html
    page = requests.get(url)

    # used to clean and sort throught the html content to get the needed data
    soup = BeautifulSoup(page.text, 'html.parser')
    # find the content in this html tag, using class_ cause class is a key world
    table = soup.find('table', class_='ssrcss-jsg8ev-TableWrapper e1icz102')

    # finds all html tags with th header
    for th in table.find_all('th'):
        # gets the text content
        title = th.text
        # appends the title to the headers
        headers.append(title)

    #creates dataframes with the headers
    top_scorers = pd.DataFrame(columns=headers)

    # finds all the html tags with tr
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [td.text.strip() for td in row_data]
        lenght = len(top_scorers)
        # gets them by row and saves to the league table dataframe
        top_scorers.loc[lenght] = row

    top_scorers.Name = top_scorers.Name.replace(r'([A-Z])', r' \1', regex=True).str.split()
    top_scorers.Name = top_scorers.Name.apply(lambda key: ' '.join(dict.fromkeys(key).keys()))

    top_scorers['Club'] = top_scorers.Name.str.split().str[2:].str.join(' ')
    top_scorers.Name = top_scorers.Name.str.split().str[:2].str.join(' ')

    col = top_scorers.pop('Club')

    top_scorers.insert(2, 'Club', col)

    top_scorers.Club = top_scorers.Club.apply(lambda mc: 'Manchester City' if 'Manchester City' in mc else mc)
    top_scorers.Club = top_scorers.Club.apply(lambda mu: 'Manchester United' if 'Manchester United' in mu else mu)
    top_scorers.Club = top_scorers.Club.apply(lambda bha: 'Brighton & Hove Albion' if 'Brighton & Hove Albion' in bha else bha)

    return top_scorers

def detail_top_scorer():
    # page link of the site were data will be extracted
    url = 'https://www.worldfootball.net/goalgetter/eng-premier-league-2023-2024/'
    # list to store the headers
    headers = []
    # makes a get request that returns the html
    page = requests.get(url)

    # used to clean and sort throught the html content to get the needed data
    soup = BeautifulSoup(page.text, 'html.parser')
    # find the content in this html tag, using class_ cause class is a key world
    table = soup.find('table', class_='standard_tabelle')

    # finds all html tags with th header
    for th in table.find_all('th'):
        # gets the text content
        title = th.text
        # appends the title to the headers
        headers.append(title)

    #creates dataframes with the headers
    detail_top_scorer = pd.DataFrame(columns=headers)

    # finds all the html tags with tr
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [td.text.strip() for td in row_data]
        lenght = len(detail_top_scorer)
        # gets them by row and saves to the league table dataframe
        detail_top_scorer.loc[lenght] = row

    detail_top_scorer = detail_top_scorer.drop([''], axis=1)
    
    detail_top_scorer.Team = detail_top_scorer.Team.str.replace('\n\n', '')

    detail_top_scorer['Penalty'] = detail_top_scorer['Goals (Penalty)'].str.split().str[-1:].str.join(' ')
    detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace('(', '')
    detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace(')', '')
    
    detail_top_scorer['Goals (Penalty)'] = detail_top_scorer['Goals (Penalty)'].str.split().str[0].str.join('')

    detail_top_scorer.rename(columns= {'Goals (Penalty)': 'Goals'}, inplace=True)

    detail_top_scorer = detail_top_scorer.drop(['#'], axis=1)

    return detail_top_scorer

def player_table():
    urls = [f'https://www.worldfootball.net/players_list/eng-premier-league-2023-2024/nach-name/{id:d}' for id in (range(1, 12))]
    # list to store dataframe columns names
    df_columns = ['Player', '', 'Team', 'born', 'Height', 'Position']

    df = pd.DataFrame(columns=df_columns)

    def player(ev):
        # page link of the site were data will be extracted
        url = ev
        # list to store the headers
        headers = []
        #makes a get request and returns the html
        page = requests.get(url)

        # used to clean and sort throught the html content to get the needed data
        soup = BeautifulSoup(page.text, 'html.parser')

        # find the content in this html tag, using class_ cause class is a key world
        table = soup.find('table', class_='standard_tabelle')

        # finds all html tags with th header
        for th in table.find_all('th'):
            # gets the text content
            title = th.text
            # appends the title to the headers
            headers.append(title)

        #creates dataframes with the headers
        players = pd.DataFrame(columns=headers)

        # finds all the html tags with tr
        for tr in table.find_all('tr')[1:]:
            row_data = tr.find_all('td')
            row = [td.text.strip() for td in row_data]
            lenght = len(players)
            # gets them by row and saves to the league table dataframe
            players.loc[lenght] = row

        return players

    for url in urls:
        player = player(url)
        df = pd.concat([df, player], axis=0).reset_index(drop=True)

    df = df.drop([''], axis=1)

    return df

def all_time_table():
    # page link of the site were data will be extracted
    url = 'https://www.worldfootball.net/alltime_table/eng-premier-league/pl-only/'
    # list to store the headers
    headers = ['pos', '#', 'Team', 'Matches', 'wins', 'Draws' 'Losses', 'Goals', 'Dif', 'Points']
    # makes a get request that returns the html
    page = requests.get(url)

    # used to clean and sort throught the html content to get the needed data
    soup = BeautifulSoup(page.text, 'html.parser')

    # find the content in this html tag, using class_ cause class is a key world
    table = soup.find('table', class_='standard_tabelle')

    # find the content in this html tag, using class_ cause class is a key world
    all_time_table = pd.DataFrame(columns=headers)

    # finds all the html tags with tr
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [td.text.strip() for td in row_data]

        if len(row) == len(headers):
            all_time_table.loc[len(all_time_table)] = row

    all_time_table = all_time_table.drop(['#'], axis=1)
    all_time_table.Team = all_time_table.Team.str.replace('\n', '')

    return all_time_table

def all_time_winner_club():
    # page link of the site were data will be extracted
    url = 'https://www.worldfootball.net/winner/eng-premier-league/'
    # list to store the headers
    headers = []
    # makes a get request that returns the html
    page = requests.get(url)

    # used to clean and sort throught the html content to get the needed data
    soup = BeautifulSoup(page.text, 'html.parser')

    # find the content in this html tag, using class_ cause class is a key world
    table = soup.find('table', class_='standard_tabelle')

    # finds all html tags with th header
    for th in table.find_all('th'):
        # gets the text content
        title = th.text
        # appends the title to the headers
        headers.append(title)

    #creates dataframes with the headers
    winners = pd.DataFrame(columns=headers)

    # finds all the html tags with tr
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [td.text.strip() for td in row_data]
        lenght = len(winners)
        # gets them by row and saves to the league table dataframe
        winners.loc[lenght] = row

    winners = winners.drop([''], axis=1)
    winners['Year'] = winners['Year'].str.replace('\n', '')

    return winners

def top_scorers_seasons():
    # page link of the site were data will be extracted
    url = 'https://www.worldfootball.net/top_scorer/eng-premier-league/'
    # list to store the headers
    headers = ['Season', '#', 'Top scorer', '#', 'Team', 'goals']
    # makes a get request that returns the html
    page = requests.get(url)

    # used to clean and sort throught the html content to get the needed data
    soup = BeautifulSoup(page.text, 'html.parser')

    # find the content in this html tag, using class_ cause class is a key world
    table = soup.find('table', class_='standard_tabelle')

    winners = pd.DataFrame(columns=headers)

    # finds all the html tags with tr
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [td.text.strip() for td in row_data]
        lenght = len(winners)
        # gets them by row and saves to the league table dataframe
        winners.loc[lenght] = row

    winners = winners.drop(['#'], axis=1)
    winners = winners.replace('\\n', '', regex=True).astype(str)
    winners['Season'] = winners['Season'].replace('', np.nan).ffill()

    return winners

def goals_per_season():
    # page link of the site were data will be extracted
    url = 'https://www.worldfootball.net/stats/eng-premier-league/1/'
    # list to store the headers
    headers = []
    # makes a get request that returns the html
    page = requests.get(url)

    # used to clean and sort throught the html content to get the needed data
    soup = BeautifulSoup(page.text, 'html.parser')

    # find the content in this html tag, using class_ cause class is a key world
    table = soup.find('table', class_='standard_tabelle')

    # finds all html tags with th header
    for th in table.find_all('th'):
        # gets the text content
        title = th.text
        # appends the title to the headers
        headers.append(title)

    #creates dataframes with the headers
    goals_per_season = pd.DataFrame(columns=headers)

    # finds all the html tags with tr
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [td.text.strip() for td in row_data]
        lenght = len(goals_per_season)

        # gets them by row and saves to the league table dataframe
        goals_per_season.loc[lenght] = row

        goals_per_season.drop(goals_per_season.index[-1], inplace=True)

        goals_per_season = goals_per_season.drop(['#'], axis=1)
        goals_per_season.rename(columns={ 'goals': 'Goals', 'Ø goals': 'Average Goals' }, inplace=True)

        return goals_per_season