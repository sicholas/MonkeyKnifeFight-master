import sched
import time
import http.client
import json
import pandas as pd
from datetime import date
from discord_webhook import DiscordWebhook, DiscordEmbed
# our files
import scrape_bets, check_for_alerts, test

def fetch_data():
    # try:
    conn = http.client.HTTPSConnection("api2-dev.betkarma.com")

    payload = ""

    headers = {
        'authority': "api2-dev.betkarma.com",
        'accept': "application/json, text/plain, */*",
        'accept-language': "en-US,en;q=0.9",
        'origin': "https://betkarma.com",
        'referer': "https://betkarma.com/",
        'sec-ch-ua-mobile': "?0",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

    curr_date = str(date.today())
    # link = f"/propsComparison?startDate={curr_date}&endDate={curr_date}&league=nfl"
    link = f'https://api2-dev.betkarma.com/propsComparison?startDate=2022-12-27&endDate=2022-12-27&league=nba'
    
    conn.request("GET", link, payload, headers)

    res = conn.getresponse()
    data = json.load(res)

    df = pd.DataFrame()

    players = {}

    for game in data['games']:
        for person in game['offers']:
            overs = []
            unders = []
            lines = []
            for outcomes in person['outcomes']:
                if outcomes['label'] == 'OVER':
                    overs.append(outcomes['last']['americanOdds'])
                    lines.append(outcomes['last']['line'])
                if outcomes['label'] == 'UNDER':
                    unders.append(outcomes['last']['americanOdds'])
            count = 0
            overs1 = []
            unders2 = []
            try:
                for i in lines:
                    if i == max(set(lines), key = lines.count):
                        overs1.append(overs[count])
                        unders2.append(unders[count])
                    count+=1
                df = pd.concat([df, pd.DataFrame.from_records([{'name':person['player'].upper() + ' ' + person['label'],'line':max(set(lines), key = lines.count), 'over':sum(overs1) / len(overs1), 'under':sum(unders2) / len(unders2)}])])
            except:
                continue
            
    return df
    # except:
    #     print('fetch_data failed; sleeping for 3 minutes')
    #     time.sleep(180)

def main():
    bets_seen = set()
    while True:
        # try:
        nick_data = fetch_data()
        print(nick_data)
        # the number of games to scrape will be the number of full games on MKF
        num_games_to_scrape = scrape_bets.get_num_full_games()
        for i in range(num_games_to_scrape):
            print('i: ' + str(i))
            ethan_data = scrape_bets.scrape(i)
    #         ethan_data = {0: [['Joel Embiid', 30.5, 'Points'], ['Julius Randle', 23.5, 'Points'], 3.0], 1: [['James Harden', 43.5, 'Fantasy Points'], ['RJ Barrett', 36.5, 'Fantasy Points'], 2.5], 2: [['RJ Barrett', 23.5, 'Points'], ['Tobias Harris', 5.5, 'Rebounds'], 2.5], 3: [['Joel Embiid', 50.5, 'Fantasy Points'], ['Julius Randle', 37.5, 'Fantasy Points'], 2.5], 4: [['Joel Embiid', 30.5, 'Points'], ['Julius Randle', 9.5, 'Rebounds'], 2.5], 5: [['Joel Embiid', 50.5, 'Fantasy Points'], ['Julius Randle', 37.5, 'Fantasy Points'], ['James Harden', 43.5, 'Fantasy Points'], 5.0], 6: [['Isaiah Hartenstein', 5.5, 'Rebounds'], 
    # ['James Harden', 9.5, 'Assists'], ['RJ Barrett', 23.5, 'Points'], 5.0], 7: [['Joel Embiid', 30.5, 'Points'], ['Julius Randle', 3.5, 'Assists'], ['Mitchell Robinson', 8.5, 'Rebounds'], 5.0], 8: [['Joel Embiid', 50.5, 'Fantasy Points'], ['Julius Randle', 37.5, 'Fantasy Points'], ['James Harden', 43.5, 'Fantasy Points'], ['RJ Barrett', 36.5, 'Fantasy Points'], 8.0], 9: [['Joel Embiid', 50.5, 'Fantasy Points'], ['Julius Randle', 37.5, 'Fantasy Points'], ['James Harden', 43.5, 'Fantasy Points'], 
    # ['RJ Barrett', 36.5, 'Fantasy Points'], ['Jalen Brunson', 34.5, 'Fantasy Points'], 15.0], 10: [['Joel Embiid', 30.5, 'Points'], ['Julius Randle', 23.5, 'Points'], ['James Harden', 9.5, 'Assists'], ['Mitchell Robinson', 8.5, 'Rebounds'], ['RJ Barrett', 23.5, 'Points'], 15.0], 11: [['Joel Embiid', 30.5, 'Points'], ['Julius Randle', 23.5, 'Points'], ['RJ Barrett', 23.5, 'Points'], ['Jalen Brunson', 20.5, 'Points'], ['James Harden', 20.5, 'Points'], ['Tobias Harris', 15.5, 'Points'], 30.0], 12: 
    # [['Joel Embiid', 50.5, 'Fantasy Points'], ['Julius Randle', 37.5, 'Fantasy Points'], ['James Harden', 43.5, 'Fantasy Points'], ['RJ Barrett', 36.5, 'Fantasy Points'], ['Jalen Brunson', 34.5, 'Fantasy Points'], ['Tobias Harris', 30.5, 'Fantasy Points'], 30.0], 13: [['Joel Embiid', 30.5, 'Points'], ['Julius Randle', 23.5, 'Points'], ['James Harden', 9.5, 'Assists'], ['Mitchell Robinson', 8.5, 'Rebounds'], ['Isaiah Hartenstein', 5.5, 'Rebounds'], ['RJ Barrett', 23.5, 'Points'], 30.0]}
            
            check_for_alerts.compare(nick_data, ethan_data, bets_seen)
        time.sleep(300)
        # except Exception as e:
        #     print('error', e)
        #     time.sleep(30)
        

if __name__ == '__main__':
    main()

    