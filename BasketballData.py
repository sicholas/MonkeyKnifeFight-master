import requests
import json


def get_data():
    url = "https://www.monkeyknifefight.com/api/v3.0.1/GET_LOBBY"

    payload = "DATA=%7B%22idSport%22%3A13%2C%22filterOptions%22%3A%7B%22szGameType%22%3A%22%22%2C%22idGameType%22%3A%22%22%2C%22dtDateTime%22%3A%22%22%7D%7D"
    headers = {
        "cookie": "PHPSESSID=6nau442pd9k0ntqo7p0rgiu8v3; AWSALB=nXT/lZslYryntbUVxuV0Q5aDOP3CpuU2fOmedDf38BxccaBlNtEJdFoSzfqv2NZsv8zc5jHcPM7OhwWQMUz1COX76uO231dZ7CJLrWDuQuf0pkhGfusPh+AbRo56; AWSALBCORS=nXT/lZslYryntbUVxuV0Q5aDOP3CpuU2fOmedDf38BxccaBlNtEJdFoSzfqv2NZsv8zc5jHcPM7OhwWQMUz1COX76uO231dZ7CJLrWDuQuf0pkhGfusPh+AbRo56",
        "authority": "www.monkeyknifefight.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "origin": "https://www.monkeyknifefight.com",
        "referer": "https://www.monkeyknifefight.com/newgame/NBA",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    mkf_data = response.json()

    return mkf_data['data']['sporting_events']


def custom_request(PHPSESSID, AWSALB, AWSALBCORS, sport):
    url = "https://www.monkeyknifefight.com/api/v3.0.1/GET_LOBBY"

    payload = "DATA=%7B%22idSport%22%3A13%2C%22filterOptions%22%3A%7B%22szGameType%22%3A%22%22%2C%22idGameType%22%3A%22%22%2C%22dtDateTime%22%3A%22%22%7D%7D"
    headers = {
        "cookie": "PHPSESSID="+PHPSESSID+"; AWSALB="+AWSALB+"; AWSALBCORS="+AWSALBCORS,
        "authority": "www.monkeyknifefight.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "origin": "https://www.monkeyknifefight.com",
        "referer": "https://www.monkeyknifefight.com/newgame/"+sport,
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    mkf_data = response.json()

    return mkf_data['data']['sporting_events']

if __name__ == '__main__':
    print(get_data())