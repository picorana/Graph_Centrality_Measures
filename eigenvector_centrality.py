import networkx as nx
import networkx.readwrite.gexf 
import json
import sys
import document_fix
from collections import defaultdict
import coloredlogs, logging
from logging import handlers
from utils import printProgressBar


subs_per_user_threshold = 5


def make_graph(sub_edges):

	logging.info("Creating graph...")

	G = nx.Graph()

	count = 0

	for idx, sub in enumerate(sub_edges):
		
		G.add_node(sub, degree=float(len(sub_edges[sub]))/float((len(sub_edges)-1)))

		for sub2 in sub_edges[sub]:
			# I think the weight of an edge should also depend on the size of the subs
			G.add_edge(sub, sub2, weight=sub_edges[sub][sub2])

		printProgressBar(idx, len(sub_edges), prefix = 'Progress:', suffix = 'Complete', length = 50)
	
	print ""

	return G


def trim_graph_edges_for_visualization(G):
	
	logging.info("Visualization trim: starting with " + str(G.number_of_edges()) + " edges")

	for node in G.nodes():
		for edge in G.edges(node):
			if G[edge[0]][edge[1]]['weight'] < 20:
				G.remove_edge(edge[0], edge[1])

	solitary= [n for n,d in G.degree_iter() if d==0]
 	G.remove_nodes_from(solitary)

	logging.info("Visualization trim: ending with " + str(G.number_of_edges()) + " edges")

	return G


def main():

	coloredlogs.install(fmt='%(asctime)s, %(hostname)s %(levelname)s %(message)s')

	logging.info("Program started")

	sub_edges = document_fix.find_edges(subs_per_user_threshold)
	sub_edges = document_fix.trim_nodes_edges(sub_edges)
	G = make_graph(sub_edges)
	#adj_matrix = adjacency_matrix(G)
	eigenvector_centrality = nx.eigenvector_centrality(G)

	for node in G.nodes():
		G.node[node]['eigenvector_centrality'] = eigenvector_centrality[node]

	G = trim_graph_edges_for_visualization(G)

	nx.write_gexf(G, "test.gexf")


if __name__ == "__main__": 
	main()