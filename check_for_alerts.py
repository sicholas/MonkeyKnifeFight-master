import pandas as pd
import time
import main
from discord_webhook import DiscordWebhook, DiscordEmbed
def expected_value(odds, multiplier):
    # Convert American odds to decimal odds
    dec_odds = []
    for odd in odds:
        if odd > 0:
            dec = odd / 100 + 1
        else:
            dec = 100 / abs(odd) + 1
        dec_odds.append(dec)

    # Calculate the fair win probability
    p_win = 1
    for dec in dec_odds:
        p_win *= 1 / dec

    # Calculate the expected value
    ev = p_win * ((multiplier - 1)) - (1 - p_win)

    return 100 * ev

# returns the line
def fantasy_points_nba(df, player_name):
    try:
        tos = df.loc[df['name'] == player_name + ' Turnovers']['line'].values[0]
    except:
        tos = 0
    try:
        pra = df.loc[df['name'] == player_name + ' Points + Rebounds + Assists']['line'].values[0]
    except:
        pra = 0
    try:
        boards = df.loc[df['name'] == player_name + ' Rebounds']['line'].values[0]
    except:
        boards = 0
    try:
        assists = df.loc[df['name'] == player_name + ' Assists']['line'].values[0]
    except:
        assists = 0
    try: 
        stocks = df.loc[df['name'] == player_name + ' Steals + Blocks']['line'].values[0]
    except:
        stocks = 0
    print(player_name, pra, boards, assists, stocks)
    return pra + .2*boards + .5*assists + 3*stocks - tos
    

def off_line_alert(player, type_bet, mkf_line, other_line, bet_array, over = 0, under = 0):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/977347618701180940/uvsWqRgOklsUSEaEp7u6wiZrVNeyCwxtmGg9vRoIXZFfz0wQBc2qrALR1CE09c1YNSTY')
    embed = DiscordEmbed(title="Line Is Off", description=f"{player} {type_bet} line is off! ", color=0x00ff11)
    embed.set_thumbnail(url="https://play-lh.googleusercontent.com/_673KT3NL07q1sC93Ii3G6l8ozxW3PDKEhFOXwHY-KFSNVGt7i7VhBRvMM9CBFaGUdep")
    embed.add_embed_field(name="MKF", value=f"{mkf_line}", inline=True)
    embed.add_embed_field(name="Other Books", value=f"{other_line}", inline=True)
    if over != 0:
        embed.add_embed_field(name="Odds", value=f"Over: {over} Under: {under}", inline=False)
    embed.add_embed_field(name="Bet Containing Player", value=f"{bet_array}", inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()
    
def ev_alert(bet_array, ev):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/977347618701180940/uvsWqRgOklsUSEaEp7u6wiZrVNeyCwxtmGg9vRoIXZFfz0wQBc2qrALR1CE09c1YNSTY')
    embed = DiscordEmbed(title="Positive EV Bet", description=f"{bet_array}", color=0x00ff11)
    embed.set_thumbnail(url="https://play-lh.googleusercontent.com/_673KT3NL07q1sC93Ii3G6l8ozxW3PDKEhFOXwHY-KFSNVGt7i7VhBRvMM9CBFaGUdep")
    embed.add_embed_field(name="EV", value=f"{ev}", inline=True)
    webhook.add_embed(embed)
    response = webhook.execute()

# book_data is nick's dataframe; mkf_data is my dictionary
def compare(book_data, mkf_data, bets_seen):
    book_data.to_csv('test.csv')
    print('comparing nick: ' + str(book_data))
    print('comparing ethan: ' + str(mkf_data))

    # loop through each bet and compare the lines
    for i in range(len(mkf_data)):
        odds = []
        size = len(mkf_data[i])
        for j in range(len(mkf_data[i])):
            mult = 0
            try:
                name = mkf_data[i][j][0].upper()
                mkf_line = mkf_data[i][j][1]
                points_type = mkf_data[i][j][2]
                
                print(f'name: {name}, points_type: {points_type}')
                
                if points_type == 'Fantasy Points':
                    book_line = fantasy_points_nba(book_data, name)
                    bet_as_string = f'{name} {points_type} {mkf_line} {book_line}'
                    
                    # ALERT if there is at least a three point difference in the lines
                    if abs(mkf_line - book_line) >= 3 and bet_as_string not in bets_seen:
                        off_line_alert(name, points_type, mkf_line, book_line, mkf_data[i])
                        bets_seen.add(bet_as_string)
                # this else means that the points type is 
                else:
                    book_line = float(book_data.loc[book_data['name'] == f"{name} {points_type}"]['line'].values[0])
                    book_odds_over = float(book_data.loc[book_data['name'] == f"{name} {points_type}"]['over'].values[0])
                    book_odds_under = float(book_data.loc[book_data['name'] == f"{name} {points_type}"]['under'].values[0])
                    bet_as_string = f'{name} {points_type} {mkf_line} {book_line}'
                    if points_type == "Points":
                        # if there is at least a two point difference in the lines
                        if abs(mkf_line - book_line) >= 2 and bet_as_string not in bets_seen:
                            off_line_alert(name, points_type, mkf_line, book_line, mkf_data[i], book_odds_over, book_odds_under)
                            bets_seen.add(bet_as_string)
                        elif abs(mkf_line - book_line) < 2: 
                            if book_odds_over < book_odds_under: odds.append(book_odds_over)
                            else: odds.append(book_odds_under)
                    # this else means that the points type is assists/rebounds/blocks 
                    else:
                        if mkf_line != book_line and bet_as_string not in bets_seen:
                            if abs(mkf_line - book_line) > 1:
                                off_line_alert(name, points_type, mkf_line, book_line, mkf_data[i], book_odds_over, book_odds_under)
                                bets_seen.add(bet_as_string)
                            elif ((mkf_line < book_line and book_odds_under > -155) or (mkf_line > book_line and -155 < book_odds_over)):
                                off_line_alert(name, points_type, mkf_line, book_line, mkf_data[i], book_odds_over, book_odds_under)
                                bets_seen.add(bet_as_string)
                        elif mkf_line != book_line: 
                            if book_odds_over < book_odds_under: odds.append(book_odds_over)
                            else: odds.append(book_odds_under)
                    
                print(f'mkf_line: {mkf_line}, book_line: {book_line}')
                    
                time.sleep(.5)
            # a TypeError means the multiplier was hit
            except TypeError:
                mult = mkf_data[i][j]
            except:
                continue
                
        if len(odds) == size:
            ev = expected_value(odds, mult)
            if ev > 3:
                ev_alert(mkf_data[i], ev)
    

if __name__ == '__main__':
    main.main()