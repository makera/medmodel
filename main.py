import networkx as nx
from functools import reduce

names = ['Агинский район', 'Акшинский район', 'Александрово-Заводский район', 'Балейский район', 'Борзинский район',
         'Газимуро-Заводский район', 'Дульдургинский район', 'Забайкальский район', 'Каларский район',
         'Калганский район', 'Карымский район', 'Краснокаменский район', 'Красночикойский район', 'Кыринский район',
         'Могойтуйский район', 'Могочинский район', 'Нерчинский район', 'Нерчинско-Заводский район',
         'Оловяннинский район', 'Ононский район', 'Петровск-Забайкальский район', 'Приаргунский район',
         'Сретенский район', 'Тунгокоченский район', 'Улётовский район', 'Хилокский район',
         'Чернышевский район', 'Читинский район', 'Шелопугинский район', 'Шилкинский район', ]
populations = [22924, 9195, 5440, 12930, 34763, 6270, 9486, 15270, 5601, 5461, 25722, 44125, 13514, 8945, 17469,
               18763, 19969, 6578, 2640, 6870, 24384, 14403, 15514, 8567, 22010, 20602, 23000, 49030, 5041, 20326, ]

G = nx.Graph()

G.add_nodes_from(nx.path_graph(names.__len__()))
edges = [(20, 25, {'weight': 160}), (25, 24, {'weight': 200}), (27, 24, {'weight': 110}), (12, 24, {'weight': 350}),
         (12, 20, {'weight': 140}), (12, 20, {'weight': 140}), (12, 25, {'weight': 270}), (13, 1, {'weight': 170}),
         (6, 1, {'weight': 75}), (6, 27, {'weight': 240}), (6, 0, {'weight': 89}), (6, 10, {'weight': 150}),
         (0, 19, {'weight': 90}), (19, 4, {'weight': 140}), (19, 18, {'weight': 130}), (0, 14, {'weight': 40}),
         (0, 27, {'weight': 160}), (0, 10, {'weight': 110}), (10, 14, {'weight': 87}), (18, 14, {'weight': 69}),
         (18, 4, {'weight': 130}), (7, 4, {'weight': 110}), (7, 11, {'weight': 90}), (21, 11, {'weight': 110}),
         (2, 11, {'weight': 160}), (9, 11, {'weight': 140}), (9, 21, {'weight': 77}), (2, 21, {'weight': 120}),
         (2, 4, {'weight': 130}), (2, 5, {'weight': 100}), (9, 17, {'weight': 79}), (5, 17, {'weight': 110}),
         (5, 28, {'weight': 94}), (2, 28, {'weight': 150}), (16, 28, {'weight': 120}), (3, 28, {'weight': 86}),
         (16, 3, {'weight': 74}), (18, 3, {'weight': 140}), (29, 14, {'weight': 120}), (29, 27, {'weight': 220}),
         (29, 10, {'weight': 150}), (27, 10, {'weight': 96}), (27, 26, {'weight': 300}), (27, 16, {'weight': 270}),
         (22, 16, {'weight': 98}), (26, 16, {'weight': 95}), (26, 22, {'weight': 81}), (27, 23, {'weight': 430}),
         (15, 26, {'weight': 290}), (29, 16, {'weight': 47}), ]
G.add_edges_from(edges)


def translate(n):
    return names[n[0]], names[n[1]]


def exclude(nodes):
    return lambda node: node not in nodes


def grouped_by_min_length(nodes, G_object):
    groups = {}
    for node in nodes:
        groups[node] = {
            'district': [],
            'length': [],
        }

    for node in filter(exclude(nodes), G_object.nodes):
        try:
            lengths = []
            for n in nodes:
                lengths.append(nx.dijkstra_path_length(G_object, n, node, 'weight'))
            groups[nodes[lengths.index(min(lengths))]]['district'].append(node)
            groups[nodes[lengths.index(min(lengths))]]['length'].append(min(lengths))
        except nx.NetworkXNoPath:
            pass
    return groups


plans = {}
key_params = {}
nodes = [27, 11]
for node in filter(exclude(nodes), G.nodes):
    plans[node] = grouped_by_min_length(nodes + [node], G)
    key_params[names[node]] = {}
    for i in nodes + [node]:
        try:
            key_params[names[node]][names[i]] = {}
            key_params[names[node]][names[i]]['districts'] = plans[node][i]['district'] + [i]
            key_params[names[node]][names[i]]['population'] = reduce(lambda prev, el: prev + populations[el],
                                                                     plans[node][i]['district'], 0) + populations[i]
            key_params[names[node]][names[i]]['districts_count'] = len(plans[node][i]['district']) + 1
            key_params[names[node]][names[i]]['max_length'] = max(plans[node][i]['length'])
            key_params[names[node]][names[i]]['min_length'] = min(plans[node][i]['length'])
            key_params[names[node]][names[i]]['avg_length'] = sum(plans[node][i]['length']) / len(
                plans[node][i]['length'])
        except:
            pass

print(key_params)
