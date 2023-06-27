import os
import networkx as nx
import signal
import sys
import tweepy as tw

import TweetGraph as twg

def tw_bearer():
#Busca o bearer token em um .txt chamado 'bearer_token'
    try:
        bearer_txt = open('bearer_token.txt')
        bearer_token = bearer_txt.readline()
    except:
    #Caso não encontre o txt digite seu bearer
        print("Você pode criar um arquivo 'bearer_token.txt' com seu token dentro!")
        bearer_token = input("Arquivo bearer_token.txt não encontrado, digite o seu bearer token: ")
    # Autenticando
    return bearer_token
   
def set_filters(query, client):
    rule = tw.StreamRule(value=query, tag= query)
    client.add_rules(rule)

def print_rules(client):
    response = client.get_rules()
    for stream_rule in response.data:
        print("Value: "+stream_rule.value+" "+"Tag: "+stream_rule.tag+" "+"Id: "+stream_rule.id+"\n")

def limpar_filtro(client):
    response = client.get_rules()
    if(response.data is not None):
        print(response)
        id_list = []
        for stream_rule in response.data:
            id_list.append(stream_rule.id)
        client.delete_rules(id_list)

def on_tweet(tweet):
    print(tweet)

def on_data(raw_data):
    print()

def save_graph(graph, filename):
    base_filename, file_extension = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}_({counter}){file_extension}"
        counter += 1
    nx.write_graphml(graph, f"{filename}")
    print(f"Grafo salvo como {filename}")

def handle_interrupt(signal, frame):
    print("Interrupção detectada. Encerrando...")
    save_graph(client.graph, "stream_graph.graphml")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)
bearer_token = tw_bearer()
client = twg.TweetGraph(bearer_token)
limpar_filtro(client)
os.system('cls') or None
query = input("Digite a sua pesquisa: ")
query = f"has:mentions {query}"
set_filters(query, client)
print('Rules atuais')
print_rules(client)
client.filter(expansions=['author_id','entities.mentions.username'], tweet_fields = ['created_at'])
input()