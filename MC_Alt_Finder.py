import requests, sys, time

antisniper_api_key = ''

class bc:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WHITE = '\u001b[37m'
    FAIL = '\033[91m'
    ENDTEXT = '\033[0m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'

def getInfo(call):
    r = requests.get(call)
    return r.json()

def process_shop_data(shop_data):
    items = shop_data.split(',')
    F_items = []

    for item in items:

        item = item.replace('_', ' ')

        item = ' '.join(word.capitalize() for word in item.split())

        item = item.replace('Ii', 'II').replace('Iii', 'III').replace('-', '-').replace('Tnt', 'TNT').replace('Null', 'Empty')

        F_items.append(item)

    return ', '.join(F_items)

while True:
    username = input("Enter the player name: ")

    AS_1 = f'https://api.antisniper.net/v2/convert/mojang?player={username}&key={antisniper_api_key}'
    data = getInfo(AS_1)

    if 'uuid' in data and data['uuid']:
        uuid = data["uuid"]
        print(f"{bc.GREEN}Player found: {bc.BLUE}{username}{bc.ENDTEXT}")
    else:
        print(f"{bc.FAIL}Player not found: {bc.BLUE}{username}{bc.ENDTEXT}")
        sys.exit()

    alt_url = f'https://api.antisniper.net/v2/player/altfinder?player={uuid}&key={antisniper_api_key}'
    data_alt = getInfo(alt_url)

    if 'data' in data_alt and data_alt['data']:
        found_usernames = []
        for user_data in data_alt['data']:
            ign = user_data['ign']

            found_usernames.append(ign)

        if len(found_usernames) > 1:
            additional_usernames = ', '.join(found_usernames[1:])
            print(f"We also found: {additional_usernames}")
            time.sleep(1)
            print(f"Fetching information for the other accounts:")
            time.sleep(1)
            print()
    else:
        print('No data or empty data in the response.')

    if 'data' in data_alt and data_alt['data']:
        found_usernames = []
        for user_data in data_alt['data']:
            ign = user_data['ign']
            shop = user_data['shop']
            discord = user_data['discord']

            F_shop = process_shop_data(shop)

            print(f"{bc.YELLOW}Account details:{bc.ENDTEXT}")
            print(f"{bc.BLUE}UUID: {bc.WHITE}{uuid}")
            print(f"{bc.BLUE}IGN: {bc.WHITE}{ign}")
            print(f"{bc.BLUE}Discord: {bc.WHITE}{discord}")
            print(f"{bc.BLUE}Shop: {bc.WHITE}{F_shop}")
            print()

    check_another = input(f"{bc.PURPLE}Do you want to check another player? (y/n): {bc.ENDTEXT}").lower()
    if check_another != 'y':
        break
