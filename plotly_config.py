

def init():
    from plotly.offline import init_notebook_mode
    init_notebook_mode(connected=True)


def loadLayout():

    from plotly.graph_objs import Layout, XAxis, YAxis

    l = Layout(
        title='<br>Network graph made with Python',
        titlefont=dict(size=16),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        annotations=[ dict(
            text="Link to the code on Github: <a href='https://github.com/picorana/Graph_Centrality_Measures'> https://github.com/picorana/Graph_Centrality_Measures</a>",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002 ) ],
        xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False))
    
    return l


def init_edge_node_trace():
    from plotly.graph_objs import Scatter, Marker, Line

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker= Marker(
            showscale=True,
            colorscale='Portland',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    return edge_trace, node_trace

def trim_graph_edges_for_visualization(G):

    for node in G.nodes():
        for edge in G.edges(node):
            if G[edge[0]][edge[1]]['weight'] < 0.045:
                G.remove_edge(edge[0], edge[1])

    solitary= [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    return G

def drawSpringLayoutGraphFromDict(G, node_sizes, coefficient=0.3):

    import networkx as nx
    from plotly.offline import iplot, init_notebook_mode
    from plotly.graph_objs import Figure, XAxis, YAxis, Data

    init_notebook_mode(connected=True)
    
    edge_trace, node_trace = init_edge_node_trace()
    
    pos = nx.spring_layout(G, k=coefficient)
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        
    node_trace['marker']['size'] = []
    
    for node in G.nodes():
        node_trace['marker']['size'].append(node_sizes[node]*500)
        node_info = 'name: ' + str(node)
        node_trace['text'].append(node_info)

    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        

    fig = Figure(data = Data([edge_trace, node_trace]), layout = loadLayout())

    iplot(fig)

def drawSpringLayoutGraph(test_G):

    import networkx as nx
    from plotly.offline import iplot, init_notebook_mode
    from plotly.graph_objs import Figure, Data, XAxis, YAxis
    
    init_notebook_mode(connected=True)

    edge_trace, node_trace = init_edge_node_trace()
    
    pos = nx.spring_layout(test_G)
    
    for edge in test_G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    for node in test_G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        
    node_trace['marker']['size'] = []
    
    for node in test_G.nodes():
        node_trace['marker']['size'].append(20)

    for node, adjacencies in enumerate(test_G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = '# AAA: '+str(len(adjacencies)) + '\n node number: ' + str(node)
        node_trace['text'].append(node_info)

    fig = Figure(data = Data([edge_trace, node_trace]), layout = loadLayout())

    iplot(fig)