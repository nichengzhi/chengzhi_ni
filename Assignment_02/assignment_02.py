from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
import random
normal_delay = random.normalvariate(2, 0.5)
import pandas as pd
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import time
from bs4 import BeautifulSoup
###Q1
driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
driver.get('http://www.mlb.com')
stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
stats_header_bar.click()
stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
time.sleep(normal_delay)
stats_line_items[0].click()
hitting_season_element = driver.find_element_by_id('sp_hitting_season')
season_select = Select(hitting_season_element)
time.sleep(normal_delay)
season_select.select_by_value('2015')
team_button = driver.find_element_by_id('st_parent')
team_button.click()
time.sleep(normal_delay)

game_type_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'st_hitting_game_type')))
#game_type_element = driver.find_element_by_id('st_hitting_game_type')
game_type_select = Select(game_type_element)
game_type_select.select_by_value("'R'")


time.sleep(normal_delay)
#team_stat_2015 = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[1]/div[8]/table/tbody')
try:
    team_stat_2015 = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[1]/div[8]/table/tbody"))
    )
    team_stat_list=[x for x in team_stat_2015.find_elements_by_tag_name('tr')]
    team_name = [e.find_element_by_class_name('dg-team_full').text for e in team_stat_list]
    team_league = [e.find_element_by_class_name('dg-league').text for e in team_stat_list]
    team_homerun = [e.find_element_by_class_name('dg-r').text for e in team_stat_list]

    team_abbrev_full = {}
    for e in team_name:
        time.sleep(normal_delay)
        team_button = driver.find_element_by_link_text(e)
        team_button.click()
        temp_tbody = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        team_abbrev = temp_tbody.find_element_by_class_name('dg-team_abbrev').text
        team_abbrev_full[team_abbrev] = e

        driver.back()
        driver.back()
        driver.back()
        time.sleep(normal_delay)

finally:
    driver.close()
teams_regular = {"name":team_name, "league":team_league, "home_run":[float(i) for i in team_homerun]}
teams_regular_data=pd.DataFrame(teams_regular)
q1_solution = teams_regular_data['name'].loc[teams_regular_data['home_run'] == teams_regular_data['home_run'].max()].values[0]
teams_regular_data.to_csv("q1andq2_a.csv")
print('the team had the most homeruns in regular season 2015 is ',q1_solution)
#q2.a
regular_league_homerun = teams_regular_data['home_run'].groupby(teams_regular_data['league']).mean().index[0]
regular_league_homerun_value = teams_regular_data['home_run'].groupby(teams_regular_data['league']).mean()[0]
print('in 2015 reguar season, the greast average number of homerun league is', regular_league_homerun,', average number of homeruns is',regular_league_homerun_value)
#q2.b firstinning
try:
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get('http://www.mlb.com')
    stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
    stats_header_bar.click()
    stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
    time.sleep(normal_delay)
    stats_line_items[0].click()
    hitting_season_element = driver.find_element_by_id('sp_hitting_season')
    season_select = Select(hitting_season_element)
    time.sleep(normal_delay)
    season_select.select_by_value('2015')
    team_button = driver.find_element_by_id('st_parent')
    team_button.click()
    time.sleep(normal_delay)

    game_type_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'st_hitting_game_type')))
    game_type_select = Select(game_type_element)
    game_type_select.select_by_value("'R'")


    time.sleep(normal_delay)
    firstinng_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "st_hitting_hitting_splits")))
    hitting_select = Select(firstinng_element)
    time.sleep(normal_delay)
    hitting_select.select_by_value("i01")
    driver.refresh()
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
finally:
    driver.close()

soup = BeautifulSoup(data_html, "html.parser")
team_name_firtinn = [e.a.string for e in soup.find_all('td', class_ = "dg-team_full")]
team_league_firstinn = [e.string for e in soup.find_all('td', class_ = "dg-league")]
team_home_run_firstinn = [e.string for e in soup.find_all('td', class_ = "dg-r")]
teams_firstinn = {"name":team_name_firtinn, "league":team_league_firstinn, "home_run":[float(i) for i in team_home_run_firstinn]}
teams_firstinn_data=pd.DataFrame(teams_firstinn)
teams_firstinn_data.to_csv("q2_b.csv")
first_inn_league = teams_firstinn_data['home_run'].groupby(teams_firstinn_data['league']).mean().index[0]
firstinn_average_homerun = teams_firstinn_data['home_run'].groupby(teams_firstinn_data['league']).mean()[0]
print('in 2015 reguarl season in firstinning, the greast average number of homerun league is', first_inn_league,', average number of homeruns is',firstinn_average_homerun)
#q3
try:
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')#q3
    driver.get('http://www.mlb.com')
    stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
    stats_header_bar.click()
    stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
    time.sleep(normal_delay)
    stats_line_items[0].click()
    hitting_season_element = driver.find_element_by_id('sp_hitting_season')
    season_select = Select(hitting_season_element)
    time.sleep(normal_delay)
    season_select.select_by_value('2017')
    time.sleep(normal_delay)
    game_type_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'sp_hitting_game_type')))
    #game_type_element = driver.find_element_by_id('st_hitting_game_type')
    game_type_select = Select(game_type_element)
    game_type_select.select_by_value("'R'")
    select_team_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'sp_hitting_team_id')))
    team_select = Select(select_team_element)
    team_select.select_by_value("147")
    driver.refresh()
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
    soup = BeautifulSoup(data_html, "html.parser")
    pler_name_nyy = [e.a.string for e in soup.find_all('td', class_ = "dg-name_display_last_init")]
    pler_pos_nyy = [e.string for e in soup.find_all('td', class_ = "dg-pos")]
    pler_pats_nyy = [e.string for e in soup.find_all('td', class_ = "dg-ab")]
    player_fullname_nyy = []
    for abrev_name in pler_name_nyy:
        time.sleep(normal_delay)
        ab_button = driver.find_element_by_link_text(abrev_name)
        ab_button.click()
        name_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'full-name')))
        player_fullname_nyy.append(name_element.text)
        driver.back()
finally:
    driver.close()
players_regular_2017_nyy = {"name":player_fullname_nyy, "pos":pler_pos_nyy, "pats":[float(i) for i in pler_pats_nyy]}
players_regular_nyy_data=pd.DataFrame(players_regular_2017_nyy)
players_regular_nyy_data.to_csv("q3.csv")
great_30 = players_regular_nyy_data[players_regular_nyy_data["pats"] > 30]
great_30.index=range(len(great_30))
print('the people who have pats great then 30 printed below:')
for i in range(len(great_30)):
    print('name: ',great_30.iloc[i,0], '. pos: ', great_30.iloc[i,2])
print("")
rf = players_regular_nyy_data[players_regular_nyy_data["pos"] == 'RF']
cf = players_regular_nyy_data[players_regular_nyy_data["pos"] == 'CF']
lf = players_regular_nyy_data[players_regular_nyy_data["pos"] == 'LF']
total_outfield = rf.append(cf, ignore_index=True).append(lf, ignore_index=True)
print('the people played in the outfield print below')
for i in range(len(total_outfield)):
    print('name: ',total_outfield.iloc[i,0], '. pos: ', total_outfield.iloc[i,2])
print("")
#q4 don't need csv, click button website will give the biggest one
try:
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get('http://www.mlb.com')
    stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
    stats_header_bar.click()
    stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
    time.sleep(normal_delay)
    stats_line_items[0].click()
    hitting_season_element = driver.find_element_by_id('sp_hitting_season')
    season_select = Select(hitting_season_element)
    time.sleep(normal_delay)
    season_select.select_by_value('2015')
    time.sleep(normal_delay)
    game_type_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'sp_hitting_game_type')))
    #game_type_element = driver.find_element_by_id('st_hitting_game_type')
    game_type_select = Select(game_type_element)
    time.sleep(normal_delay)
    game_type_select.select_by_value("'R'")
    al_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sp_hitting-1 > fieldset:nth-child(1) > label:nth-child(4)')))
    al_button.click()
    ab_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'th.dg-ab')))
    ab_button.click()
    driver.refresh()
    """select_team_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'sp_hitting_team_id')))
    team_name"""
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
    soup = BeautifulSoup(data_html, "html.parser")
    the_one_name = soup.tbody.tr.find('td', class_ = 'dg-name_display_last_init').a.string
    the_one_pos = soup.tbody.tr.find('td', class_ = 'dg-pos').string
    the_one_team = team_abbrev_full[soup.tbody.tr.find('td', class_ = 'dg-team_abbrev').string.strip()]
    ab_button = driver.find_element_by_link_text(the_one_name)
    ab_button.click()
    the_one_full_name = driver.find_element_by_class_name('full-name').text
finally:
    driver.close()
print('the one who had the most bats in 2015 is',the_one_full_name,'his team name is',the_one_team,'his position is',the_one_pos)
#q5
try:
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get('http://www.mlb.com')
    stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
    stats_header_bar.click()
    stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
    time.sleep(normal_delay)
    stats_line_items[0].click()
    hitting_season_element = driver.find_element_by_id('sp_hitting_season')
    season_select = Select(hitting_season_element)
    time.sleep(normal_delay)
    season_select.select_by_value('2014')
    time.sleep(normal_delay)
    game_type_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'sp_hitting_game_type')))
    #game_type_element = driver.find_element_by_id('st_hitting_game_type')
    game_type_select = Select(game_type_element)
    time.sleep(normal_delay)
    game_type_select.select_by_value("'A'")
    driver.refresh()
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
    soup = BeautifulSoup(data_html, "html.parser")
    player_name_at = [e.a.string for e in soup.find_all('td', class_ = "dg-name_display_last_init")]
    player_team_at = []
    player_info = []
    for name in player_name_at:
        ab_button = driver.find_element_by_link_text(name)
        ab_button.click()
        time.sleep(normal_delay)
        name_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'player-bio')))
        ul = name_element.find_elements_by_tag_name("ul")
        bio_info = ul[0].text
        player_info.append(bio_info)
        time.sleep(normal_delay)
        career_stats = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'careerStats')))
        batting_stats = career_stats.find_element_by_tag_name('tbody')
        sit_2017 =  batting_stats.find_elements_by_tag_name('tr')[-1]
        player_team_at.append(sit_2017.find_elements_by_tag_name('td')[1].text)
        driver.back()
finally:
    driver.close()
as_player_fullname = [e.split('\n')[0] for e in player_info]
as_player_bornplace = []
for e in player_info:
    info = e.split('\n')
    for inf in info:
        if 'Born' in inf:
            as_player_bornplace.append(inf.split(',')[1])

player_fullteam_at = []
for e in player_team_at:
    try:
        player_fullteam_at.append(team_abbrev_full[e])
    except KeyError:
        player_fullteam_at.append(e)
players_as_2014 = {"name":as_player_fullname,  "born place":as_player_bornplace, 'team':player_fullteam_at, 'abbrev name':player_name_at}
players_as_data=pd.DataFrame(players_as_2014)
# use google search get the latin american countries list
try:
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get('http://www.google.com')
    time.sleep(2)
    input = driver.find_element_by_name('q')
    input.send_keys('latin america')
    input.submit()
    time.sleep(3)
    latin_wiki = driver.find_element_by_link_text('Latin America - Wikipedia')
    latin_wiki.click()
    countries_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[4]/div/table[2]/tbody')))
    trs = countries_element.find_elements_by_tag_name('tr')
    countries_list = []
    for tr in trs:
        tds = tr.find_elements_by_tag_name('td')
        countries_list.append(tds[2].text)
finally:
    driver.close()
latin_players = pd.DataFrame(columns = players_as_data.columns)
for i in range(len(players_as_data)):
    if players_as_data.iloc[i,1].strip() in countries_list:
        latin_players = latin_players.append(players_as_data.iloc[i], ignore_index=True)
latin_players.to_csv("q5.csv")
q5_answer = 'name:{}, born place:{}, team:{}'
print('latin america player printed below')
for i in range(len(latin_players)):
    print(q5_answer.format(latin_players.iloc[i,2], latin_players.iloc[i,1], latin_players.iloc[i,3]))
#q6
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '1f7d1c1c10564dc0bb1a9fdfcf2cf1ca',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", "/v3/mlb/stats/{JSON}/Games/{2016}?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    # print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
data_json = data.decode('utf8').replace("'", '"')
with open("Question_6_schedule.json", 'w') as outfile:
    json.dump(data_json, outfile)

team_game_info = json.loads(data_json)
hou_2016_games = pd.DataFrame(columns=['opponent Team name abbrev','game date','stadium id'])
count = 0
for game in team_game_info:
    if game['AwayTeam'] == 'HOU':
        hou_2016_games.loc[count] = [game['HomeTeam'], game['Day'], game['StadiumID']]
        count += 1
    elif game['HomeTeam'] == 'HOU':
        hou_2016_games.loc[count] = [game['AwayTeam'], game['Day'], game['StadiumID']]
        count += 1
    else:
        pass
try:
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", "/v3/mlb/stats/{JSON}/Stadiums?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data_stadium = response.read()
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
data_stadium__json = data_stadium.decode('utf8').replace("'", '"')
with open("Question_6_stadium.json", 'w') as outfile:
    json.dump(data_stadium__json, outfile)
stadium_info = json.loads(data_stadium__json)
id_name ={}
id_city = {}
id_state = {}
for stadium in stadium_info:
    id_name[stadium['StadiumID']] = stadium['Name']
    id_city[stadium['StadiumID']] = stadium['City']
    id_state[stadium['StadiumID']] = stadium['State']
hou_2016_games['stadium_name'] = [id_name[e] for e in hou_2016_games['stadium id']]
hou_2016_games['stadium_city'] = [id_city[e] for e in hou_2016_games['stadium id']]
hou_2016_games['stadium_state'] = [id_state[e] for e in hou_2016_games['stadium id']]
q6_answer = '<{}><{}><{}><{}>,<{}>'
for i in range(len(hou_2016_games)):
    #onegame = hou_2016_games.loc[i]
    print(q6_answer.format(hou_2016_games.iloc[i,0], hou_2016_games.iloc[i,1], hou_2016_games.iloc[i,3], hou_2016_games.iloc[i,4],hou_2016_games.iloc[i,5]))