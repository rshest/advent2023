# DAY25
import networkx as nx

f = open('input/25.txt', 'r')
lines = [line.strip() for line in f.readlines()]


def parse_line(line):
    parts = line.split(':')
    name = parts[0].strip()
    children = [p.strip() for p in parts[1].split()]
    return name, children


def complete_graph(graph):
    res = {}
    for node, to in graph.items():
        for dst in to:
            if dst not in res:
                res[dst] = [node]
            else:
                res[dst].append(node)
            if node not in res:
                res[node] = [dst]
            else:
                res[node].append(dst)
    return res


def get_edges(graph):
    res = set()
    for src in graph.keys():
        for dst in graph[src]:
            if (dst, src) not in res:
                res.add((src, dst))
    return list(res)


def get_partitions(edges, exclude):
    res = []
    for e in edges:
        e1, e2 = e
        if (e1, e2) in exclude or (e2, e1) in exclude:
            continue
        found = False
        for s in res:
            if (e1 in s) or (e2 in s):
                s.add(e1)
                s.add(e2)
                found = True
                break
        if not found:
            print(e, res)
            p = set()
            p.add(e1)
            p.add(e2)
            res.append(p)
    return res


graph = [parse_line(line) for line in lines]
graph = {name: to for name, to in graph}
graph = complete_graph(graph)
edges = get_edges(graph)

G = nx.Graph()

G.add_nodes_from(graph.keys())
G.add_edges_from(edges)

min_edges = nx.minimum_edge_cut(G)
for edge in min_edges:
    G.remove_edge(edge[0], edge[1])

counts = [G.subgraph(c).number_of_nodes() for c in nx.connected_components(G)]
res2 = counts[0] * counts[1]
print(res2)
