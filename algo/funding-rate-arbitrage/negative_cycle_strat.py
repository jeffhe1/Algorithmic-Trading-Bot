import itertools
from pybit.unified_trading import HTTP
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from operator import itemgetter
from functools import reduce

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret_key= os.getenv("API_SECRET_KEY") 

class NegativeCycleStrat:
    def __init__(self, api_key:str, api_secret_key:str, **kwargs) -> None:
        """
        api_key: API key
        api_secret_key: API secret key
        """
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.session = HTTP(
            testnet=kwargs.get('testnet', False),
            api_key=api_key,
            api_secret=api_secret_key,
            demo=kwargs.get('demo', False))
    
    def create_adjacency_matrix(self, category:str = 'spot', **kwargs) -> dict:
        """
        creates adjacency matrix from the graph
        """
        plot:bool = kwargs.get('plot', False)
        results = self.session.get_instruments_info(category=category)['result']['list']
        coin_pairs:list[tuple[str]] = [(result['baseCoin'], result['quoteCoin']) for result in results]
        graph:dict = {}
        
        for value, key in coin_pairs:
            if key not in graph.keys():
                graph[key] = []
            graph[key].append(value)
        
        coins : list[list]= np.unique(list(itertools.chain(*itemgetter(*list(graph.keys())[1:])(graph), list(graph.keys())))) # connected non-leaf coins
        combs : list[set] = [set(comb) for comb in itertools.combinations(coins, 2)]
        edges : list[tuple]= [[[pair[0], pair[1], 1], [pair[1], pair[0], -1]] for pair in coin_pairs if set(pair) in combs]
        """
        shows plot
        """
        if plot:
            G=nx.DiGraph()
            G.add_weighted_edges_from(edges)
            nx.draw(G, with_labels=True)
            plt.show()
        return edges
        
        
    def update_weights(self, edges:list, **kwargs) -> list[tuple] :
        """
        updates weights based on the adjacency matrix
        bid: highest buy price
        ask: lowest sell price
        """
        result = self.session.get_tickers(category='spot')['result']['list']
        new_edges:list[tuple] = []
        for coin_pairs in edges:
            symbol = coin_pairs[0][0] + coin_pairs[0][1]
            coin_pairs[0][2] = np.log((float(result[[result.index(item) for item in result if item['symbol'] == symbol][0]]['bid1Price'])))
            coin_pairs[1][2] = np.log(1/(float(result[[result.index(item) for item in result if item['symbol'] == symbol][0]]['ask1Price'])))
            new_edges.append(tuple(coin_pairs[0]))
            new_edges.append(tuple(coin_pairs[1]))
        return new_edges
    
    def get_negative_paths(self, edges:list, **kwargs):
        G = nx.MultiDiGraph()
        G.add_weighted_edges_from(edges)
        if kwargs.get('plot', False):
            nx.draw(G, with_labels=True)
            plt.show()

        paths:list[list] = []
        coin_specifier = kwargs.get("coin", None)
        
        if coin_specifier == None: 
            for node in G.nodes():
                try: 
                    paths.append(nx.find_negative_cycle(G, node))
                except nx.NetworkXError as e:
                    continue
        else:
            paths.append(nx.find_negative_cycle(G, coin_specifier))
        print(paths)
        for path in paths:
            pairs = [(path[i], path[i+1]) for i in range(len(path)-1)]
            path.append((sum(itemgetter(*pairs)(nx.get_edge_data(G, "weight")))))
            print(path)
            
        nx.get_edge_attributes(G, "weight")
    
ncs = NegativeCycleStrat(api_key, api_secret_key)
edges = ncs.create_adjacency_matrix()
edges = ncs.update_weights(edges)
print(edges)
ncs.get_negative_paths(edges, coin="USDT")