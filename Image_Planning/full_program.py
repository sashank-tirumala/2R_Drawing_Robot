# import pandas as pd
# import networkx as nx
# name = 'square'
# df = pd.read_csv('used_by_program/'+name+'.csv')
# # print(df)
# node_dic={}
# i=0
# node1=[]
# node2=[]
# weight=[]
# for index, rows in df.iterrows():
#     tup1 = (rows['x1'],rows['y1'])
#     tup2 =(rows['x2'],rows['y2'])
#     # print(tup1)
#     weight.append(round(rows['weight'],3))
#     if tup1 in node_dic:
#         # print("is present")
#         node1.append(node_dic[tup1])
#     else:
#         # print("created node: ",i)
#         node_dic[tup1]=i
#         node1.append(node_dic[tup1])
#         i=i+1
#     if tup2 in node_dic:
#         # print("is present")
#         node2.append(node_dic[tup2])
#
#     else:
#         # print("created node: ",i)
#         node_dic[tup2]=i
#         node2.append(node_dic[tup2])
#         i=i+1
#
#
#
# current_df = pd.DataFrame({'node1':node1,'node2':node2,'weight':weight})
# current_df.to_csv(sep=",",index=False, path_or_buf='ans2.csv')
# G = nx.Graph()
# print("creating graph")
# for index, rows in current_df.iterrows():
#     G.add_node(rows['node1'])
#     G.add_node(rows['node2'])
#     G.add_edge(rows['node1'],rows['node2'],weight=rows['weight'])
# inv_node_dic = {v: k for k, v in node_dic.items()}
# print("completed inverting the node, starting to write string")
# u = 0
# adj_str = ""
# req_str = ""
# # while(u<len(node_dic)):
# #     adj_str = adj_str + ','
# #     req_str = req_str + ','
# #     adj_str = adj_str+str(u)
# #     req_str =req_str+ "1"
# #     u = u+1
# # adj_str = adj_str +"\n"
# # req_str =req_str+ "\n"
# u=0
# while(u<len(node_dic)):
#     v=0
#     # adj_str = adj_str+str(u)
#     # req_str=req_str+"1"
#     while(v<len(node_dic)):
#         if(v == 0):
#             nothing =1
#         else:
#             adj_str = adj_str + ','
#             req_str = req_str + ','
#         x1 = inv_node_dic[u][0]
#         x2 = inv_node_dic[v][0]
#         y1 = inv_node_dic[u][1]
#         y2 = inv_node_dic[v][1]
#         if(u == v):
#             dist = -1
#         else:
#             dist =int(((x2-x1)**2 +(y2-y1)**2)**0.5)
#         adj_str = adj_str + str(dist)
#         if((u,v) in G.edges):
#             req_str = req_str+"1"
#         else:
#             req_str = req_str+"0"
#         v=v+1
#     adj_str=adj_str+"\n"
#     req_str=req_str+"\n"
#     u=u+1
#
# final_adj  = open('used_by_program/'+name+'_mc'+'.csv','w')
# final_req  = open('used_by_program/'+name+'_mc_required'+'.csv','w')
# final_adj.write(adj_str)
# final_req.write(req_str)
#
#

# Montecarlo.py

from GraphUtils import *
from random import *
import time
import math
import re
verbose = True  # enable/disable verbose mode
name = 'square_mc'
print(name)
g = Graph(filename="used_by_program/"+name)

# configuration variables
max_it = 25
iteration_counter = 0
alpha = 1

# shortest tour found
shortest_tour = None
shortest_tour_path = None
shortest_tour_cost = math.inf

start_time = time.clock()
iter_c = 0
while iteration_counter < max_it:
    iteration_counter += 1
    # tour[i][j] holds the count of how many times edge (i, j) was traversed
    tour = [[0 for col in range(g.num_vertices)] for row in range(g.num_vertices)]
    tour_path = Path(g)
    edge_required = [[False for col in range(g.num_vertices)] for row in range(g.num_vertices)]
    for edge in g.get_required():
        edge_required[edge[0]][edge[1]] = True
        edge_required[edge[1]][edge[0]] = True

    cost = 0
    num_required = len(g.get_required())
    # probabilities[i][j] holds probability of traversing edge (i, j)
    probabilities = [[0 for col in range(g.num_vertices)] for row in range(g.num_vertices)]
    for v1 in range(0, g.num_vertices):
        for v2 in range(v1, g.num_vertices):
            weight = g.get_weight(v1, v2)
            if weight > 0:
                probabilities[v1][v2] = weight ** -alpha
            else:
                probabilities[v1][v2] = 0

    # randomly place the "vehicle" on a vertex
    current_pos = randint(0, g.num_vertices-1)
    starting_pos = current_pos
    tour_path.extend(starting_pos)
    if verbose: print("Starting at %s" % current_pos)
    while num_required > 0:
        neighbors = g.get_neighbors(current_pos)
        type_1_edges = g.get_type_1_edges(current_pos, edge_required)
        type_2_edges = g.get_type_2_edges(current_pos, edge_required)

        selected_edge = None

        if len(type_1_edges) > 0:
            # randomly pick a type 1 edge to traverse - all T1 edges have equal probability to be selected
            if verbose: print("Choosing type 1 edge")
            selection = randint(0, len(type_1_edges)-1)
            selected_edge = type_1_edges[selection]
        elif len(type_2_edges) > 0:
            # pick a type 2 vertex based on their probabilities
            if verbose: print("Choosing type 2 edge")
            prob_sum = 0
            for edge in type_2_edges:
                prob_sum += probabilities[edge[0]][edge[1]]
            selection = random() * prob_sum
            prob_sum = 0
            for edge in type_2_edges:
                prob_sum += probabilities[edge[0]][edge[1]]
                if selection <= prob_sum:
                    selected_edge = edge
                    break
        else:
            # randomly select a neighboring edge based on their probabilities
            if verbose: print("Choosing another edge")
            prob_sum = 0
            for neighbor in neighbors:
                prob_sum += probabilities[current_pos][neighbor]
            selection = random() * prob_sum
            prob_sum = 0
            for neighbor in neighbors:
                prob_sum += probabilities[current_pos][neighbor]
                if selection <= prob_sum:
                    selected_edge = (current_pos, neighbor)
                    break

        # we have selected an edge to traverse
        if verbose: print("Traversing edge", selected_edge)
        if edge_required[selected_edge[0]][selected_edge[1]]:
            edge_required[selected_edge[0]][selected_edge[1]] = False
            edge_required[selected_edge[1]][selected_edge[0]] = False
            num_required -= 1

        # traverse the edge
        tour[selected_edge[0]][selected_edge[1]] += 1
        tour[selected_edge[1]][selected_edge[0]] += 1
        tour_path.extend(selected_edge[1])
        cost += g.get_weight(selected_edge[0], selected_edge[1])
        current_pos = selected_edge[1]
    # end while

    # we've now traversed all required edges
    # complete the tour by adding a copy of each edge on the shortest path from current_pos to the starting_pos
    shortest_path_to_beginning = djikstra(g, current_pos)[starting_pos]
    for edge in shortest_path_to_beginning.get_edges():
        tour[edge[0]][edge[1]] += 1
        tour[edge[1]][edge[0]] += 1
        tour_path.extend(edge[1])
        cost += g.get_weight(edge[0], edge[1])

    # SR1
    if verbose: print("Cost before SR1: %s" % cost)
    for vertex1 in range(0, len(tour)):
        for vertex2 in range(0, len(tour)):
            while tour[vertex1][vertex2] > 3:
                tour[vertex1][vertex2] -= 2
                tour[vertex2][vertex1] -= 2
                cost -= g.get_weight(vertex1, vertex2)
    if verbose: print("Cost before SR1: %s" % cost)

    # SR2
    # create graph object for this tour used to find connected components - this is not an accurate representation of the tour as a subgraph!
    if verbose: print("Cost before SR2: %s" % cost)
    tour_graph = Graph(adjacency_matrix=tour, required_matrix=[[]], consider_zero_disconnected=True)
    for vertex1 in range(0, len(tour)):
        for vertex2 in range(0, len(tour)):
            if not g.is_required(vertex1, vertex2) and tour[vertex1][vertex2] == 2:
                reachable_before = bfs(tour_graph, vertex1)
                tour_graph.representation[vertex1][vertex2] = None
                reachable_after = bfs(tour_graph, vertex1)
                if len(reachable_after) == len(reachable_before):  # graph is still connected
                    tour[vertex1][vertex2] = 0
                    tour[vertex2][vertex1] = 0
                    cost -= 2 * g.get_weight(vertex1, vertex2)
                else:
                    tour_graph.representation[vertex1][vertex2] = 2

    if verbose: print("Cost after SR2: %s" % cost)

    # SR3
    if verbose: print("Cost before SR3: %s" % cost)
    double_edge = None
    for vertex1 in range(0, len(tour)):
        for vertex2 in range(0, len(tour)):
            if tour[vertex1][vertex2] == 2:
                double_edge = (vertex1, vertex2)
                break
    if double_edge is not None:
        double_path = Path(tour_graph, double_edge[0])
        double_path.extend(double_edge[1])
        expansion_found = True
        while expansion_found:
            end_vertex = double_path.vertices[-1]
            neighbors = tour_graph.get_neighbors(end_vertex)
            expansion_found = False
            for neighbor in neighbors:
                if neighbor not in double_path.vertices and tour[end_vertex][neighbor] == 2:
                    expansion_found = True
                    double_path.extend(neighbor)
                    break
        # remove one copy of each edge in double_path and add an edge along the shortest path
        start_vertex = double_path.vertices[0]
        end_vertex = double_path.vertices[-1]
        for edge in double_path.get_edges():
            tour[edge[0]][edge[1]] -= 1
            tour[edge[1]][edge[0]] -= 1
            cost -= g.get_weight(edge[0], edge[1])
        for edge in djikstra(g, start_vertex)[end_vertex].get_edges():
            tour[edge[0]][edge[1]] += 1
            tour[edge[1]][edge[0]] += 1
            cost += g.get_weight(edge[0], edge[1])


    if verbose: print("Cost after SR3: %s" % cost)

    if verbose: print("Found tour with cost %s" % cost)

    if cost < shortest_tour_cost:
        shortest_tour = tour
        shortest_tour_path = tour_path
        shortest_tour_cost = cost
    print('completed iteration: ',iter_c)
    iter_c = iter_c + 1
# end outer while


time_elapsed = time.clock() - start_time

print("Done searching!\nBest tour found has cost %s" % shortest_tour_cost)
print("Path before simplification routines:\n %s" % shortest_tour_path)
txt_file = open('used_by_program/'+name+'_sol.txt','w')
txt_file.write(str(shortest_tour_path))
print("Time elapsed: %s ms" % (time_elapsed*1000))
txt_file = open('used_by_program/'+name+'_sol.txt','r')
parse = txt_file.read()
parse = parse.split(' -> ')
parse_int=[]
for x in parse:
    parse_int.append(int(x))

i=0
parsed = []
for x in parse_int:
    if(i != len(parse_int) - 1):
        tup1 = (x,parse_int[i+1])
        parsed.append(tup1)
    i = i+1
str1="node1,node2\n"
for x in parsed:
    str1 = str1+str(x[0])+","+str(x[1])+"\n"

txt_file = open('used_by_program/'+name+'_parsed_sol.txt','w')
txt_file.write(str1)
txt_file.close()



# check_sol.py

import pandas as pd
import networkx as nx
import re

# ans parameters below --------
# to print when not drawing becuase it is a repeated edge
repeat_edge_string = "u\n"
connect_edge_string = "u\n"
draw_edge_string = "d\n"
is_first_point = True

df = pd.read_csv('used_by_program/square.csv')
# print(df)
node_dic={}
i=0
node1=[]
node2=[]
weight=[]
for index, rows in df.iterrows():
    tup1 = (rows['x1'],rows['y1'])
    tup2 =(rows['x2'],rows['y2'])
    # print(tup1)
    weight.append(round(rows['weight'],3))
    if tup1 in node_dic:
        # print("is present")
        node1.append(node_dic[tup1])
    else:
        # print("created node: ",i)
        node_dic[tup1]=i
        node1.append(node_dic[tup1])
        i=i+1
    if tup2 in node_dic:
        # print("is present")
        node2.append(node_dic[tup2])

    else:
        # print("created node: ",i)
        node_dic[tup2]=i
        node2.append(node_dic[tup2])
        i=i+1



current_df = pd.DataFrame({'node1':node1,'node2':node2,'weight':weight})
current_df.to_csv(sep=",",index=False, path_or_buf='ans2.csv')
G1 = nx.Graph()
print("creating graph")
for index, rows in current_df.iterrows():
    G1.add_node(int(rows['node1']))
    G1.add_node(int(rows['node2']))
    G1.add_edge(rows['node1'],rows['node2'],weight=rows['weight'])
inv_node_dic = {v: k for k, v in node_dic.items()}

df2 = pd.read_csv('used_by_program/'+name+'_parsed_sol.txt')
G2 = nx.Graph()
final_sol =''
s1 = set()
for index, rows in df2.iterrows():
    G2.add_node(rows['node1'])
    G2.add_node(rows['node2'])
    G2.add_edge(rows['node1'],rows['node2'])
    tup1 = (rows['node1'], rows['node2'])
    tup2 = (rows['node2'], rows['node1'])
    if((rows['node1'],rows['node2']) in s1):
        if(is_first_point):
            final_sol = final_sol +'0.0,0.0,'+str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+'u\n'
            #final_sol = final_sol +str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+str(inv_node_dic[rows['node2']][0])+','+str(inv_node_dic[rows['node2']][1])+','+draw_edge_string

            is_first_point = False
        else:
            final_sol = final_sol +str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+str(inv_node_dic[rows['node2']][0])+','+str(inv_node_dic[rows['node2']][1])+','+repeat_edge_string
    else:
        if(is_first_point):
            #Add origin and first point
            if(tup1 in G1.edges or tup2 in G1.edges):
                final_sol = final_sol +'0.0,0.0,'+str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+'u\n'
            else:
                final_sol = final_sol ++'0.0,0.0,'+str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+'u\n'
            #Add first and second point
            if(tup1 in G1.edges or tup2 in G1.edges):
                final_sol = final_sol +str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+str(inv_node_dic[rows['node2']][0])+','+str(inv_node_dic[rows['node2']][1])+','+draw_edge_string
            else:
                final_sol = final_sol +str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+str(inv_node_dic[rows['node2']][0])+','+str(inv_node_dic[rows['node2']][1])+','+connect_edge_string

            is_first_point = False
        else:
            if(tup1 in G1.edges or tup2 in G1.edges):
                final_sol = final_sol +str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+str(inv_node_dic[rows['node2']][0])+','+str(inv_node_dic[rows['node2']][1])+','+draw_edge_string
            else:
                final_sol = final_sol +str(inv_node_dic[rows['node1']][0])+','+str(inv_node_dic[rows['node1']][1])+','+str(inv_node_dic[rows['node2']][0])+','+str(inv_node_dic[rows['node2']][1])+','+connect_edge_string
        s1.add((rows['node1'],rows['node2']))
        s1.add((rows['node2'],rows['node1']))
# print(G1.edges())
# print(G2.edges())
yes = 0
no = 0
did_not_visit=[]
for x in G1.edges():
    y=str(x)
    y=re.findall('\d+',y)
    tup1 = (int(y[0]),int(y[1]))
    tup2 = (int(y[1]),int(y[0]))
    if(tup1 in G2.edges or tup2 in G2.edges):
        yes = yes + 1
    else:
        no = no + 1
        did_not_visit.append(x)

percent_accuracy = yes*100/(yes + no)
str1 = 'visited '+str(yes) +' no of edges out of '+ str(yes + no) + '\n' +'This solution is: '+str(percent_accuracy)+' accurate'
print(str1)
print(did_not_visit)
txt_file = open('final/'+name+'_final_solution.txt','w')
txt_file.write(final_sol)
txt_file.close()
