import json
from datetime import datetime

# Učitavanje podataka iz direct-messages.js
with open('direct-messages-formatted.js', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Učitavanje podataka o nalogu
with open('account.js', 'r', encoding='utf-8') as file:
    account_data = json.load(file)

# Funkcija za generisanje izveštaja
def generate_report(data, start_date, end_date):
    report = f"Razgovori putem Twitter aplikacije\nDatum i vreme obrade: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += f"Analiza objavljena za nalog korisnika čiji je ID: {account_data[0]['account']['accountId']}, a korisničko ime: {account_data[0]['account']['username']}\n\n"
    for conversation in data:
        conversation_id = conversation['dmConversation']['conversationId']
        participants = conversation_id.split('-')  
        report += f"Razgovor između korisnika: {' i '.join(participants)}\n"

        for message in conversation['dmConversation']['messages']:
            sender_id = message['messageCreate']['senderId']
            text = message['messageCreate']['text']
            created_at = datetime.strptime(message['messageCreate']['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

            if start_date <= created_at <= end_date:
                report += f"{created_at.strftime('%Y-%m-%d %H:%M')}   |   {sender_id.ljust(20)}   |   {text}\n"

        report += "\n"

    return report

# Unos početnog i krajnjeg datuma pretrage
start_date_input = input("Unesite početni datum pretrage (DD.MM.YYYY): ")
end_date_input = input("Unesite krajnji datum pretrage (DD.MM.YYYY): ")

# Pretvaranje unetih datuma u datetime objekte
start_date = datetime.strptime(start_date_input, '%d.%m.%Y')
end_date = datetime.strptime(end_date_input, '%d.%m.%Y')

# Generisanje izveštaja
report_text = generate_report(data, start_date, end_date)

# Čuvanje izveštaja u tekstualnu datoteku
with open('twitter_report3.txt', 'w', encoding='utf-8') as file:
    file.write(report_text)

print("Izveštaj je uspešno generisan.")
