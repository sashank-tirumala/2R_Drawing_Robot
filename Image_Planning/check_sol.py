import pandas as pd
import networkx as nx
import re

# ans parameters below --------
# to print when not drawing becuase it is a repeated edge
repeat_edge_string = "u\n"
connect_edge_string = "u\n"
draw_edge_string = "d\n"
is_first_point = True
name = 'square_mc'

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
txt_file = open('final_solution.txt','w')
txt_file.write(final_sol)
txt_file.close()
