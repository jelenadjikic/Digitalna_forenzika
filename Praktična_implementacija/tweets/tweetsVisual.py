import json
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# Učitavanje podataka iz fajla
with open('tweets.js', 'r', encoding='utf-8') as file:
    tweets_data = json.load(file)

# Kreiranje praznog grafa
G = nx.Graph()

# Inicijalizacija brojača objavljenih postova po satu, danu, mesecu
posts_per_hour = [0] * 24
posts_per_day = [0] * 31 
posts_per_month = [0] * 12

# Procesiranje svakog tvita
for tweet in tweets_data:
    # Izvlačenje datuma tvita
    tweet_date = datetime.strptime(tweet['tweet']['created_at'], '%a %b %d %H:%M:%S %z %Y')

    # Ažuriranje statistike po satu
    posts_per_hour[tweet_date.hour] += 1

    # Ažuriranje statistike po danu
    posts_per_day[tweet_date.day - 1] += 1  

    # Ažuriranje statistike po mesecu
    posts_per_month[tweet_date.month - 1] += 1  
    
# Vizualizacija statistike aktivnosti
plt.figure(figsize=(15, 5))

# Vizualizacija po satu u danu
plt.subplot(1, 3, 1)
plt.plot(range(24), posts_per_hour, marker='o')
plt.title('Broj objavljenih postova po satu u danu')
plt.xlabel('Sat')
plt.ylabel('Broj objavljenih postova')

# Vizualizacija po danima u mesecu
plt.subplot(1, 3, 2)
plt.plot(range(1, 32), posts_per_day, marker='o')
plt.title('Broj objavljenih postova po danu u mesecu')
plt.xlabel('Dan')
plt.ylabel('Broj objavljenih postova')

# Vizualizacija po mesecima u godini
plt.subplot(1, 3, 3)
plt.plot(range(1, 13), posts_per_month, marker='o')
plt.title('Broj objavljenih postova po mesecu u godini')
plt.xlabel('Mesec')
plt.ylabel('Broj objavljenih postova')

plt.tight_layout()
plt.show()
