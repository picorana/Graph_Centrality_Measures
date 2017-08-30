import json
import logging
from collections import defaultdict
from utils import printProgressBar

users_file = open("./partial/users.txt", 'r')
defaults = json.load(open("./partial/defaults.json", 'r'))

def find_edges(subs_per_user_threshold, overwrite=False, lines_read_threshold=5000):

	logging.info("Retrieving edge list...")

	sub_edges = {}
	edge_counter = 0

	for idx, line in enumerate(users_file):

		user = line.strip().split("\t")[0]
		if len(line.strip().split("\t"))==1: continue
		sublist = line.strip().split("\t")[1].split(" ")

		# the user posted in too few subs
		if len(sublist) < subs_per_user_threshold: continue

		# the user posted in too many subs
		if len(sublist) > 400: continue

		for sub in sublist:
			sub = sub.split("::")[0]

			if sub not in sub_edges: 
				sub_edges[sub] = defaultdict(int)
			
			for sub2 in sublist:
				sub2 = sub2.split("::")[0]
				if sub!=sub2: sub_edges[sub][sub2] += 1
				edge_counter += 1

		printProgressBar(idx, lines_read_threshold, prefix = 'Progress:', suffix = 'Complete', length = 50)
		
		if idx >= lines_read_threshold: break

	print ""	
	logging.info("Found " + str(len(sub_edges)) + " nodes and " + str(edge_counter) + " edges")
	
	# TODO: better manage saving partial files
	if overwrite: 
		json.dump(sub_edges, open("./partial/edges.json", 'w+'))
	
	return sub_edges


def trim_nodes_edges(sub_edges, overwrite=False):

	edge_weight_threshold = 10
	node_degree_threshold = 1

	new_sub_edges = {}
	edge_counter = 0

	logging.info("trimming " + str(len(sub_edges)) + " nodes...")

	for idx, sub in enumerate(sub_edges):
		if sub in defaults: continue

		this_sub_edge_dict = defaultdict(int)

		for sub2 in sub_edges[sub]:
			
			if sub2 in defaults: continue

			if sub_edges[sub][sub2] > edge_weight_threshold:
				this_sub_edge_dict[sub2] = sub_edges[sub][sub2]
				edge_counter += 1

		if len(this_sub_edge_dict) > node_degree_threshold:
			new_sub_edges[sub] = this_sub_edge_dict

		printProgressBar(idx, len(sub_edges), prefix = 'Progress:', suffix = 'Complete', length = 50)

	print ""
	logging.info("reduced to " + str(len(new_sub_edges)) + " nodes.")

	if overwrite:
		json.dump(new_sub_edges, open("./partial/edges_trimmed.json", 'w+'))
	

	return new_sub_edges

"""
#find_edges(subs_per_user_threshold)
sub_edges = json.load(open('./partial/edges.json'))
sub_edges = trim_nodes_edges(sub_edges)
#sub_edges = json.load(open('./partial/edges_trimmed.json'))
"""

