import facebook

access_token = "EAACEdEose0cBAEliLasALsr8oZB6L0S37x0RHbOa0qj3OVxonzSVrK2pWLwGrFi9Q9gQZChhCIdlXRu32iZAZCrC15z9GXcZAX7AxhJIrZAZCAfO1RW5x66Fj91Bp1xr75g5UfdoWkq52EqnIUUbZADVQ3CymhHYHvCgwDZCXski4QsVm8V0i1WeyodtZCRUI4VOwZBSWw64dERgwZDZD"

graph = facebook.GraphAPI(access_token=access_token)

friends = graph.get_all_connections("me", "friends")

edgelist = []

for friend in friends:
	edgelist.append(["Rana Di Bartolomeo", friend['name']])

result = open("facebook_edgelist.txt", 'w+')
for edge in edgelist:
	result.write(edge[0].encode('utf-8', errors='ignore') + '\t' + edge[1].encode('utf-8', errors='ignore') + '\n')