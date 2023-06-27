import tweepy as tw
import networkx as nx

class TweetGraph(tw.StreamingClient):
     
    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.graph = nx.Graph()

    def on_tweet(self, tweet):
        info = tweet_informations(tweet)
        print(f"{tweet.id} ({tweet.author_id}): {tweet.text}")
        print("-"*50)
        for mentioned in info[4]:
            self.graph.add_edge(info[0], mentioned)

def tweet_informations(response):
    mencoes = []
    if "entities" in response:
        if 'mentions' in response.entities:
            for mencao in response.entities['mentions']:
                mencoes.append(mencao['id'])

        output = [response.author_id, response.created_at, response.id, response.text, mencoes]
        return output