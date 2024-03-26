import json
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import math

# Učitavanje korisnikovog accountID iz fajla account.js
with open('account.js', 'r', encoding='utf-8') as file:
    account_data = json.load(file)
account_id = account_data[0]['account']['accountId']
account_username = account_data[0]['account']['username']

# Učitavanje podataka o praćenjima i pratiocima korisnika account_id
with open('following.js', 'r', encoding='utf-8') as file:
    following_data = json.load(file)

with open('follower.js', 'r', encoding='utf-8') as file:
    follower_data = json.load(file)

# Učitavanje podataka o konverzacijama
with open('direct-messages-formatted.js', 'r', encoding='utf-8') as file:
    conversations_data = json.load(file)

# Kreiranje praznog usmerenog grafa za raspored u krugu
G_circle = nx.DiGraph()

# Dodavanje centralnog čvora za korisnika account_id
G_circle.add_node(account_id, pos=(0, 0))

unique_users = set()
for following in following_data:
    unique_users.add(following['following']['accountId'])
for follower in follower_data:
    unique_users.add(follower['follower']['accountId'])
num_nodes = len(unique_users)
radius = 5  # Poluprečnik kruga

for i, following in enumerate(following_data):
    following_id = following['following']['accountId']
    angle = 2 * math.pi * (i / num_nodes)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    G_circle.add_node(following_id, pos=(x, y))
    G_circle.add_edge(account_id, following_id, weight=0)
    
for i, follower in enumerate(follower_data):
    follower_id = follower['follower']['accountId']
    if follower_id not in G_circle:
        angle = 2 * math.pi * ((i + len(following_data)) / num_nodes)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        G_circle.add_node(follower_id, pos=(x, y))
    if not G_circle.has_edge(follower_id, account_id):
        G_circle.add_edge(follower_id, account_id, weight=0)


# Unos početnog i krajnjeg datuma pretrage
start_date_input = input("Unesite početni datum pretrage (DD.MM.YYYY): ")
end_date_input = input("Unesite krajnji datum pretrage (DD.MM.YYYY): ")

# Pretvaranje unetih datuma u datetime objekte
start_date = datetime.strptime(start_date_input, '%d.%m.%Y')
end_date = datetime.strptime(end_date_input, '%d.%m.%Y')

# Dodavanje težina na grane u grafu
for conversation in conversations_data:
    conversation_id = conversation['dmConversation']['conversationId']
    messages = conversation['dmConversation']['messages']
    message_count = 0
    # Provera da li su poruke između početnog i krajnjeg datuma
    for message in messages:
        message_date = datetime.strptime(message['messageCreate']['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if start_date <= message_date <= end_date:
            # Brojanje poruka u konverzaciji
            message_count +=1
            # Provera da li je korisnik account_id učestvovao u konverzaciji
            participants = [message['messageCreate']['senderId'] for message in messages]
            if account_id in participants:
                # Pronalaženje ID-ja korisnika s kojim je korisnik razmenjivao poruke
                other_user_id = participants[0] if participants[1] == account_id else participants[1]
                
    # Ažuriranje težine na grani 
    if G_circle.has_edge(account_id, other_user_id):
        G_circle.edges[account_id, other_user_id]['weight'] += message_count

    if G_circle.has_edge(other_user_id, account_id):
        G_circle.edges[other_user_id, account_id]['weight'] += message_count

# Lista čvorova sa kojima je razmenjena makar jedna poruka
nodes_with_messages = [node_id for node_id, data in G_circle.nodes(data=True) 
                       if 'pos' in data and G_circle.out_degree(node_id) > 0]

plt.figure(figsize=(10, 10))
pos_circle = nx.get_node_attributes(G_circle, 'pos')
edge_labels_circle = nx.get_edge_attributes(G_circle, 'weight')
node_colors = ['yellow' if node_id == account_id else 'green' 
               if node_id in nodes_with_messages else 'red' for node_id in G_circle.nodes]

nx.draw(G_circle, pos_circle, with_labels=True, node_color=node_colors, node_size=500, arrowsize=10, font_size=7)
nx.draw_networkx_edge_labels(G_circle, pos_circle, edge_labels=edge_labels_circle)
plt.title('Graf praćenja korisnika raspoređen u krugu (težine predstavljene brojem poruka)')
plt.show()
