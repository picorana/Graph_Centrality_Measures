import networkx as nx

G = nx.read_edgelist(open('data/edgelist_weighted.txt', 'rb'))

G2 = nx.Graph()

nsfw_subs = []
for line in open('data/nsfw_subs.txt', 'rb'):
	nsfw_subs.append(line.strip())

print nsfw_subs

for edge in G.edges(data=True):
	if edge[0] not in nsfw_subs and edge[1] not in nsfw_subs:
		G2.add_edge(edge[0], edge[1], weight=edge[2]['weight'])

nx.write_edgelist(G2, open('data/edgelist_weighted_clean.txt', 'w+'))