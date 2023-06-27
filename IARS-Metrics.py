import tweepy as tw
import networkx as nx
import time

# Definir credenciais da API do Twitter
bearer_token= 'AAAAAAAAAAAAAAAAAAAAAMx%2FMwEAAAAAXe22nDyS0kaPVscFN2DE%2BUy6jOE%3DraoBo6BEHi1RrprC9AJTfyXE786vRPWjn8iiHXuUMJYXze6B6Q'

# Autenticando
client = tw.Client(bearer_token)

i = 0

# Como não possuo Twitter peguei um amigo meu como ego da rede
username_ego = "kbrianps"

def acharId(username):

  response = client.get_user(username = username_ego)
  id_ego = response.data['id']
  return id_ego

# Retorna a lista de quem um usuário segue
def retornaListaSeguindo(id_usuario):
  time.sleep(120)
  print(i)
  response = client.get_users_following(id = id_usuario, max_results = 20)
  lista_seguindo = []
  if (response.data is not None):
    for usuario in response.data:
      usuario_dict = {}
      usuario_dict[0] = usuario.id
      usuario_dict[1] = usuario.username
      lista_seguindo.append(usuario_dict)
    return lista_seguindo
  
def get_seguidores(id_usuario):
    user = client.get_user(id=id_usuario, user_fields=['public_metrics'])
    return user.data.public_metrics['followers_count']

seguindo_nivel_1 = retornaListaSeguindo(acharId(username_ego))

#Cria um grafo direcionado
egonet = nx.DiGraph()

#Crio o nó do ego e adiciono o seu atributo de seguidores
egonet.add_node(username_ego)
seguidores_ego = get_seguidores(acharId(username_ego))
egonet.nodes[username_ego]['Seguidores'] = seguidores_ego

for seguido in seguindo_nivel_1:

    egonet.add_node(seguido[1])
    print(i)
    i += 1
    seguidores = get_seguidores(seguido[0])
    egonet.nodes[seguido[1]]['Seguidores'] = seguidores

  # Adiciono uma aresta ligando os nós
    egonet.add_edge(username_ego,seguido[1])
  
  #obtenho a lista de seguidores do nó atual
    seguindo_nivel_2 = retornaListaSeguindo(seguido[0])
    if (seguindo_nivel_2 is not None):
        for seguido_nivel_2 in seguindo_nivel_2:

            egonet.add_node(seguido_nivel_2[1])
            seguidores = get_seguidores(seguido_nivel_2[0])
            egonet.nodes[seguido_nivel_2[1]]['Seguidores'] = seguidores

        # Adiciono uma aresta ligando os nós
            egonet.add_edge(seguido[1],seguido_nivel_2[1])

nx.write_graphml_lxml(egonet, "ego_net.graphml")

for no in egonet.nodes():
    print(f"Seguidores do nó {no}: {egonet.nodes[no]['Seguidores']}")
