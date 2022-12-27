import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
from IPython.display import display

import BasketballData


# returns selenium driver
def get_driver():
    options = Options()
    # options.add_argument("--headless")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    return driver

# returns a list of each "full game" when given a specific sport
def get_full_games():
    data = BasketballData.get_data()
    full_games = []
    # adds all Full Games to the full_games list
    for i, game in data.items():
        if game['segment'] == 'Full Game':
            full_games.append(game)
    
    return full_games


def get_num_full_games():
    full_games = get_full_games()
    return len(full_games)


def bets_to_dataframe(bets, driver):
    i = 0
    bets_dict = {}
    # create pandas dataframe
    pd.set_option("display.max_rows", 1000)
    df = pd.DataFrame()
    
    multipliers = driver.find_elements_by_xpath("//*[@class='MuiTypography-root MuiTypography-arvoBoldItalic css-vll2jz']")
    legs = driver.find_elements_by_xpath("//*[@class='MuiTypography-root MuiTypography-arvoBoldItalic css-d98nbk']")
    
    for k in range(len(bets)):
        bet = bets[k]
        multiplier = multipliers[k].text
        leg = legs[k].text
        
        bet.click()
        time.sleep(.2)
        bet_info = driver.find_element_by_xpath("//*[@class='MuiGrid-root MuiGrid-container css-1d3bbye']")
        players = driver.find_elements_by_xpath("//*[@class='MuiGrid-root MuiGrid-item css-5j8ind']")
        
        # check to see if goal is 2/2, 3/3, etc.
        if leg[0] == leg[2]:
            for j in range(len(players)):
                # index 0: name, index 1: line, index 2: type of points
                players[j] = players[j].text.split('\n')
                # convert the line from a string to a float
                players[j][1] = float(players[j][1])
            
            try:
                bets_dict[i] = players
                bets_dict[i].append(float(multiplier.replace('x','')))
            except IndexError:
                print("INDEX OUT OF RANGE: SCRAPE_BETS.PY")
            
            i += 1
        
        time.sleep(.25)
        
        # try close bet info window
        try:
            driver.find_element_by_xpath("//*[@class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-1he8ulx']").click()
        except:
            driver.find_element_by_xpath("//*[@class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-36iqlp']").click()
        
        
        df = pd.concat([df, pd.DataFrame.from_records([bets_dict])])
        
        time.sleep(.25)
        # break
    
    # display(df.to_string())
    print(bets_dict)
    print('--------------------------------------------------------------')
    
    return bets_dict
    
# essentailly the main function
# the index parameter is used to choose which full game will be scraped
def scrape(index):
    driver = get_driver()
    # bets_dict will store all the bets
    bets_dict = {}
    # dictionary to keep track of the int used with each sport in MKF links
    sport_ints = {'basketball': 13}
    # get_full_games will return a list of each "full game" when given a specific sport
    full_games = get_full_games()
    # for i in range(len(full_games)):
        
    gameID = full_games[index]['iGameCodeGlobalId']
    sport_int = sport_ints["basketball"]
    
    url = f'https://www.monkeyknifefight.com/game/{sport_int}/{gameID}/ml'
    
    driver.get(url)
    
    bets = driver.find_elements_by_xpath("//*[@class='MuiGrid-root MuiGrid-container css-1pgi2q5']")
    
    return bets_to_dataframe(bets, driver)

    
if __name__ == '__main__':
    scrape()