import pandas as pd
import requests
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
        row = [td.text for td in row_data]
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
        row = [td.text for td in row_data]
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
        row = [td.text for td in row_data]
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

    print(detail_top_scorer)
    return detail_top_scorer

detail_top_scorer()