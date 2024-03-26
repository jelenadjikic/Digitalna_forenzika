import json
from datetime import datetime, timezone

with open('tweets.js', 'r', encoding='utf-8') as file:
    tweets = json.load(file)

keyword = input("Unesite ključnu reč za pretragu: ")
start_date_input = input("Unesite početni datum pretrage (DD.MM.YYYY): ")
end_date_input = input("Unesite krajnji datum pretrage (DD.MM.YYYY): ")

start_date = datetime.strptime(start_date_input, '%d.%m.%Y').replace(tzinfo=timezone.utc)
end_date = datetime.strptime(end_date_input, '%d.%m.%Y').replace(tzinfo=timezone.utc)

# Pronalaženje tweetova koji sadrže ključnu reč i spadaju u odabrani vremenski interval
matching_tweets = [tweet for tweet in tweets if keyword.lower() in tweet['tweet']['full_text'].lower() 
                   and start_date <= datetime.strptime(tweet['tweet']['created_at'], '%a %b %d %H:%M:%S %z %Y') <= end_date]

# Upisivanje pronađenih tweetova u fajl
output_filename = f"{keyword}_tweets.txt"
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(f"Created at       | Favorites | Tweet \n")
    for tweet in matching_tweets:
        # Formatiranje datuma u lepši format
        formatted_date = datetime.strptime(tweet['tweet']['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%d.%m.%Y %H:%M')

        file.write(f"{formatted_date} | {tweet['tweet']['favorite_count'].ljust(9)} |{tweet['tweet']['full_text']}\n")

print(f"Pronađeni tweetovi koji sadrže ključnu reč '{keyword}' i koji su objavljeni u periodu od {start_date.strftime('%d.%m.%Y')} do {end_date.strftime('%d.%m.%Y')} su upisani u fajl '{output_filename}'.")
