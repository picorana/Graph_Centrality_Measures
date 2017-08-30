import networkx as nx
import networkx.readwrite.gexf 
import json
import sys
import document_fix
from collections import defaultdict
import coloredlogs, logging
from logging import handlers



subs_per_user_threshold = 100

G = nx.Graph()

def make_graph(sub_edges):
	count = 0

	for sub in sub_edges:
		
		G.add_node(sub, degree=float(len(sub_edges[sub]))/float((len(sub_edges)-1)))

		for sub2 in sub_edges[sub]:
			if sub_edges[sub][sub2] > 200: G.add_edge(sub, sub2)

		count += 1


def main():

	coloredlogs.install(fmt='%(asctime)s, %(hostname)s %(levelname)s %(message)s')

	logging.info("Program started")

	sub_edges = document_fix.find_edges(subs_per_user_threshold)
	make_graph(sub_edges)

	nx.write_gexf(G, "test.gexf")


if __name__ == "__main__": 
	main()